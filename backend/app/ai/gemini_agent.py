"""Generación con Gemini, function calling manual y eventos de progreso."""

from __future__ import annotations

import asyncio
import logging
import time
from collections.abc import AsyncIterator, Callable
from typing import Any

import pydantic
from google.genai import errors as genai_errors
from google.genai import types

from app.ai.gemini_client import MODEL, TOOLS, client
from app.core.config import settings
from app.schemas.agent_response import AgentResponse

logger = logging.getLogger(__name__)

EventCallback = Callable[[dict[str, Any]], None]

MAX_TOOL_TURNS = 12
TOOL_MAP = {tool.__name__: tool for tool in TOOLS}

# Errores transitorios de Gemini: saturación (503), límite de cuota (429) y
# fallos internos (500, 504). Otros códigos (400, 403...) no se reintentan:
# repetir una petición mal formada o sin permiso daría el mismo error.
RETRYABLE_CODES = {429, 500, 503, 504}


class ModelCaller:
    """Llama a Gemini con reintentos y modelo de respaldo (harness del agente).

    Cada error transitorio se reintenta con espera exponencial
    (`GEMINI_RETRY_BASE_SECONDS` × 1, × 2, × 4...). Si el modelo principal
    agota sus reintentos, se pasa al modelo de respaldo y se sigue usando ese
    durante el resto de la pregunta, para no pagar de nuevo las esperas en
    cada turno del bucle de herramientas.
    """

    def __init__(
        self,
        models: list[str] | None = None,
        max_retries: int | None = None,
        base_delay: float | None = None,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        if models is None:
            models = [MODEL]
            if settings.GEMINI_FALLBACK_MODEL and settings.GEMINI_FALLBACK_MODEL != MODEL:
                models.append(settings.GEMINI_FALLBACK_MODEL)
        self.models = models
        self.max_retries = settings.GEMINI_MAX_RETRIES if max_retries is None else max_retries
        self.base_delay = settings.GEMINI_RETRY_BASE_SECONDS if base_delay is None else base_delay
        self._sleep = sleep
        self._index = 0

    @property
    def model(self) -> str:
        return self.models[self._index]

    def __call__(self, contents: list[types.Content], config: dict[str, Any]):
        last_error: genai_errors.APIError | None = None
        while self._index < len(self.models):
            for attempt in range(self.max_retries + 1):
                try:
                    return client.models.generate_content(model=self.model, contents=contents, config=config)
                except genai_errors.APIError as error:
                    if error.code not in RETRYABLE_CODES:
                        raise
                    last_error = error
                    if attempt < self.max_retries:
                        delay = self.base_delay * 2**attempt
                        logger.warning(
                            "gemini_retry model=%s code=%s intento=%d espera=%.1fs",
                            self.model, error.code, attempt + 1, delay,
                        )
                        self._sleep(delay)
            if self._index + 1 < len(self.models):
                logger.warning("gemini_fallback de %s a %s", self.model, self.models[self._index + 1])
            self._index += 1
        assert last_error is not None
        raise last_error


def _tool_config(system_instruction: str | None) -> dict[str, Any]:
    # Dict config: el SDK de genai interpreta disable:True de forma fiable.
    return {
        "system_instruction": system_instruction,
        "tools": TOOLS,
        "automatic_function_calling": {
            "disable": True,
            "ignore_call_history": True,
        },
    }


def _structured_config(system_instruction: str | None) -> dict[str, Any]:
    return {
        "system_instruction": system_instruction,
        "response_mime_type": "application/json",
        "response_json_schema": AgentResponse.model_json_schema(),
        "automatic_function_calling": {"disable": True},
    }


def _execute_tool(name: str, args: dict[str, Any] | None) -> Any:
    tool = TOOL_MAP.get(name)
    if tool is None:
        return {"error": f"Unknown tool: {name}"}

    kwargs = dict(args) if args else {}
    return tool(**kwargs)


def generate_with_events(
    prompt: str,
    system_instruction: str | None = None,
    on_event: EventCallback | None = None,
) -> AgentResponse:
    """Ejecuta el agente con tools manuales y emite eventos reales de progreso."""

    emit = on_event or (lambda _event: None)
    emit({"type": "status", "phase": "thinking"})

    contents: list[types.Content] = [
        types.Content(role="user", parts=[types.Part.from_text(text=prompt)]),
    ]

    call_model = ModelCaller()

    for _turn in range(MAX_TOOL_TURNS):
        response = call_model(contents, _tool_config(system_instruction))

        if not response.candidates:
            break

        candidate = response.candidates[0]
        if not candidate.content or not candidate.content.parts:
            break

        function_calls = [part.function_call for part in candidate.content.parts if part.function_call]
        if function_calls:
            contents.append(candidate.content)
            response_parts: list[types.Part] = []

            for function_call in function_calls:
                name = function_call.name or "unknown_tool"
                logger.info("tool_call name=%s", name)
                emit({"type": "tool_call", "tool": name})
                result = _execute_tool(name, function_call.args)
                emit({"type": "tool_done", "tool": name})
                response_parts.append(
                    types.Part.from_function_response(
                        name=name,
                        response={"result": result},
                    )
                )

            contents.append(types.Content(role="user", parts=response_parts))
            continue

        text = (response.text or "").strip()
        if text:
            try:
                parsed = AgentResponse.model_validate_json(text)
            except pydantic.ValidationError:
                # El borrador en texto libre se descarta: la conversación no puede
                # terminar en un turno del modelo (Gemini 3.5 lo rechaza con 400) y
                # la llamada estructurada lo regenera desde los resultados de las tools.
                break
            else:
                emit({"type": "status", "phase": "synthesizing"})
                return parsed

        break

    emit({"type": "status", "phase": "synthesizing"})
    final = call_model(contents, _structured_config(system_instruction))
    return AgentResponse.model_validate_json(final.text)


async def stream_answer_events(
    prompt: str,
    system_instruction: str | None = None,
) -> AsyncIterator[dict[str, Any]]:
    """Async generator de eventos SSE para el frontend."""

    loop = asyncio.get_running_loop()
    queue: asyncio.Queue[dict[str, Any] | None] = asyncio.Queue()

    def on_event(event: dict[str, Any]) -> None:
        # generate_with_events corre en un worker thread: hay que encolar de forma thread-safe.
        loop.call_soon_threadsafe(queue.put_nowait, event)

    async def run_generation() -> None:
        try:
            result = await asyncio.to_thread(
                generate_with_events,
                prompt,
                system_instruction,
                on_event,
            )
            await queue.put({"type": "done", "response": result.model_dump()})
        except genai_errors.APIError as error:
            await queue.put({"type": "error", "message": f"Gemini API error: {error}"})
        except pydantic.ValidationError as error:
            await queue.put(
                {
                    "type": "error",
                    "message": f"Gemini devolvió una respuesta inválida: {error}",
                }
            )
        except Exception as error:  # noqa: BLE001 — propagar mensaje al cliente SSE
            await queue.put({"type": "error", "message": str(error)})
        finally:
            await queue.put(None)

    yield {"type": "started"}

    task = asyncio.create_task(run_generation())
    while True:
        event = await queue.get()
        if event is None:
            break
        yield event

    await task
