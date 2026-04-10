@echo off
REM Crear entorno virtual y instalar requerimientos
py -m venv ejecucion_presupuestal
if exist ejecucion_presupuestal\Scripts\activate.bat (
    call ejecucion_presupuestal\Scripts\activate.bat
    pip install --upgrade pip
    pip install -r requirements.txt
    echo Entorno ejecucion_presupuestal creado e instalaciones completadas.
) else (
    echo Error creando el entorno virtual ejecucion_presupuestal.
)
pause
