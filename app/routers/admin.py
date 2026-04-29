from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database import get_db

router = APIRouter()


@router.post("/truncate-all")
def truncate_all_tables(db: Session = Depends(get_db)):
    """
    Elimina todos los datos de las tablas (TRUNCATE) pero conserva la estructura.
    Las tablas truncadas son: cdp, crp, eje
    """
    try:
        # Desactivar restricciones de clave foránea temporalmente
        db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
        
        # Truncate de todas las tablas
        tables = ["cdp", "crp", "eje"]
        for table in tables:
            db.execute(text(f"TRUNCATE TABLE {table}"))
        
        # Reactivar restricciones de clave foránea
        db.execute(text("SET FOREIGN_KEY_CHECKS=1"))
        
        db.commit()
        return {
            "success": True,
            "message": "Todas las tablas han sido truncadas exitosamente.",
            "tables_cleared": tables
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error durante el truncate: {str(e)}"
        )


@router.post("/truncate/{table_name}")
def truncate_table(table_name: str, db: Session = Depends(get_db)):
    """
    Trunca (elimina datos) de una sola tabla permitida, preservando la estructura.
    Tabla a truncar: debe estar en la lista permitida: cdp, crp, eje
    """
    allowed_tables = {"cdp", "crp", "eje"}
    if table_name not in allowed_tables:
        raise HTTPException(status_code=400, detail=f"Tabla no permitida: {table_name}")

    try:
        # Desactivar temporalmente las restricciones de FK
        db.execute(text("SET FOREIGN_KEY_CHECKS=0"))

        # Ejecutar truncate seguro
        db.execute(text(f"TRUNCATE TABLE `{table_name}`"))

        # Reactivar restricciones
        db.execute(text("SET FOREIGN_KEY_CHECKS=1"))

        db.commit()
        return {"success": True, "message": f"Tabla {table_name} truncada correctamente.", "table_cleared": table_name}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error truncando {table_name}: {str(e)}")
