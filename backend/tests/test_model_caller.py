from types import SimpleNamespace

import pytest
from google.genai import errors as genai_errors

from app.ai import gemini_agent
from app.ai.gemini_agent import ModelCaller


def _error(code: int) -> genai_errors.APIError:
    return genai_errors.APIError(code, {"error": {"code": code, "message": "x", "status": "X"}})


class FakeModels:
    """Sustituye a client.models: devuelve, por modelo, una lista de resultados."""

    def __init__(self, script: dict[str, list]):
        self.script = script
        self.calls: list[str] = []

    def generate_content(self, model, contents, config):
        self.calls.append(model)
        outcome = self.script[model].pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome


@pytest.fixture
def fake(monkeypatch):
    def install(script):
        models = FakeModels(script)
        monkeypatch.setattr(gemini_agent, "client", SimpleNamespace(models=models))
        return models

    return install


def make_caller(sleeps):
    return ModelCaller(models=["principal", "respaldo"], max_retries=2, base_delay=1.0, sleep=sleeps.append)


def test_retries_transient_errors_with_exponential_backoff(fake):
    models = fake({"principal": [_error(503), _error(429), "respuesta"]})
    sleeps: list[float] = []

    assert make_caller(sleeps)([], {}) == "respuesta"
    assert models.calls == ["principal"] * 3
    assert sleeps == [1.0, 2.0]


def test_falls_back_and_sticks_to_backup_model(fake):
    models = fake({"principal": [_error(503)] * 3, "respaldo": ["r1", "r2"]})
    sleeps: list[float] = []
    caller = make_caller(sleeps)

    assert caller([], {}) == "r1"
    assert caller([], {}) == "r2"  # el siguiente turno va directo al respaldo
    assert models.calls == ["principal"] * 3 + ["respaldo"] * 2
    assert caller.model == "respaldo"


def test_non_transient_errors_are_not_retried(fake):
    models = fake({"principal": [_error(400)]})

    with pytest.raises(genai_errors.APIError):
        make_caller([])([], {})
    assert models.calls == ["principal"]


def test_raises_last_error_when_every_model_fails(fake):
    fake({"principal": [_error(503)] * 3, "respaldo": [_error(503)] * 3})

    with pytest.raises(genai_errors.APIError) as info:
        make_caller([])([], {})
    assert info.value.code == 503
