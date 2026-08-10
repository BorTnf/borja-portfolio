"""Punto de entrada para levantar el servidor de desarrollo con uvicorn.

Uso:
    python run.py
"""

import os
from pathlib import Path

import uvicorn

os.chdir(Path(__file__).resolve().parent)

from app.core.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        reload_dirs=["app"],
    )
