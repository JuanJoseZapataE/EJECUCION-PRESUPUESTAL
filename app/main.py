from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .routers import cdp, crp, eje, admin

app = FastAPI(title="API Presupuesto")

# CORS para permitir llamadas desde el frontend (file:// o mismo host)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # desarrollo: permitir todo
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cdp.router, prefix="/cdp", tags=["CDP"])
app.include_router(crp.router, prefix="/crp", tags=["CRP"])
app.include_router(eje.router, prefix="/eje", tags=["EJE"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])


@app.get("/")
async def root():
    return {"message": "API Presupuesto funcionando"}


# Servir archivos estáticos del frontend
frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
if frontend_dir.exists():
    app.mount("/frontend", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")


@app.get("/dashboard", include_in_schema=False)
async def dashboard():
    """Devuelve el index.html del frontend como página principal del dashboard."""
    index_path = frontend_dir / "index.html"
    return FileResponse(str(index_path))
