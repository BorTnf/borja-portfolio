# Despliegue

El proyecto se despliega en dos plataformas:

- **Frontend** → **Cloudflare Pages** (sitio estático + CDN global) — producción: [borja-portfolio.pages.dev](https://borja-portfolio.pages.dev/)
- **Backend** → **Render** (API FastAPI, plan Free) — producción: [borja-portfolio-api.onrender.com](https://borja-portfolio-api.onrender.com)

El orden recomendado es **primero el backend** (para tener su URL pública) y **después el frontend** (que necesita esa URL en `PUBLIC_API_URL`).

Ambos servicios están conectados al repo de GitHub (`BorTnf/borja-portfolio`): cada `git push` a `master` redespliega automáticamente Render y Cloudflare Pages.

> **Plan Free de Render:** el servicio se "duerme" tras 15 minutos de inactividad. La primera petición tras dormirse puede tardar hasta ~50s en responder — es el cold start, no un error.

---

## 1. Backend en Render

### Configuración del servicio

- **Root directory:** `backend`
- **Start command:** `python run.py`

`run.py` levanta Uvicorn leyendo `HOST`, `PORT` y `RELOAD` desde `Settings` (que a su vez los toma del entorno). Render inyecta la variable `PORT` automáticamente; hay que setear `HOST=0.0.0.0` para aceptar conexiones externas (el default `127.0.0.1` solo acepta conexiones locales y Render marcaría el servicio como caído).

### Variables de entorno (Render → Environment)

| Variable | Valor en producción |
|---|---|
| `GEMINI_API_KEY` | tu API key de Google Gemini |
| `HOST` | `0.0.0.0` |
| `ENVIRONMENT` | `production` |
| `RELOAD` | `false` |
| `BACKEND_CORS_ORIGINS` | `["https://borja-portfolio.pages.dev", "http://localhost:4321"]` (lista JSON con el dominio del frontend) |

> `PORT` lo provee Render; no hace falta setearlo a mano.

> **Importante:** si `BACKEND_CORS_ORIGINS` no incluye el dominio exacto del frontend, el navegador bloqueará las peticiones por CORS. Incluir también dominios de preview de Cloudflare si quieres que funcionen.

### Verificación

- `https://borja-portfolio-api.onrender.com/health` → `{"status": "ok"}`
- `https://borja-portfolio-api.onrender.com/docs` → Swagger UI

---

## 2. Frontend en Cloudflare Pages

### Configuración del build

- **Root directory:** `frontend`
- **Framework preset:** Astro
- **Build command:** `npm run build`
- **Build output directory:** `dist`

Astro genera un sitio **estático** (`dist/`), que Cloudflare Pages sirve directamente desde su CDN.

### Variables de entorno (Cloudflare Pages → Settings → Environment variables)

| Variable | Valor en producción |
|---|---|
| `PUBLIC_API_URL` | `https://borja-portfolio-api.onrender.com` |

> Las variables `PUBLIC_*` se inyectan en el bundle en **build time**. Si cambias `PUBLIC_API_URL`, hay que **volver a buildear** (redeploy) para que tome efecto. Nunca poner secretos en variables `PUBLIC_*`: viajan al cliente.

### Verificación

- El sitio carga en el dominio de Pages.
- Al hacer una pregunta en el asistente, en la pestaña Network del navegador se ve el request a `/api/v1/chat/stream` contra la URL de Render respondiendo `200` (y no un error de CORS).

---

## Checklist de un release

1. `GEMINI_API_KEY` configurada en Render (nunca en el repo).
2. `BACKEND_CORS_ORIGINS` incluye el dominio de Cloudflare Pages.
3. `PUBLIC_API_URL` en Cloudflare apunta al backend de Render y se hizo redeploy.
4. `/health` del backend responde OK.
5. El asistente responde en el sitio en producción sin errores de CORS.

---

## Troubleshooting

| Síntoma | Causa probable | Solución |
|---|---|---|
| El chat no responde y la consola muestra error de CORS | El dominio del frontend no está en `BACKEND_CORS_ORIGINS` | Agregarlo (lista JSON) y redeploy del backend |
| El chat pega contra `localhost:8000` en producción | `PUBLIC_API_URL` no seteada o no se rebuildeó | Setear la variable en Cloudflare y redeploy |
| `429 Too Many Requests` | Rate limit (10 req/min por IP) | Esperar un minuto; ajustar en `app/core/rate_limiter.py` si hace falta |
| El backend arranca pero Render lo marca como caído | Uvicorn escuchando en `127.0.0.1` | Setear `HOST=0.0.0.0` en Render |
| `502` desde el frontend, o la primera respuesta tarda ~50s | El backend estaba dormido (plan Free) o no pudo responder (API key inválida, cuota de Gemini) | Reintentar tras el cold start; si persiste, revisar logs de Render y `GEMINI_API_KEY` |
