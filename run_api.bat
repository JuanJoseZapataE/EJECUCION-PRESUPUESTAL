@echo off
REM Activar entorno y ejecutar FastAPI con Uvicorn
if not exist ejecucion_presupuestal (
    echo No existe el entorno ejecucion_presupuestal. Ejecute primero setup_env.bat
    pause
    exit /b 1
)

call ejecucion_presupuestal\Scripts\activate.bat
set PORT=8000
start "Presupuesto" http://127.0.0.1:%PORT%/dashboard
uvicorn app.main:app --reload --host 127.0.0.1 --port %PORT%
