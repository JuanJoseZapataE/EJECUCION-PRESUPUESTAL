from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
import pandas as pd
from io import BytesIO

from app.database import get_db
from app.models import CDP

router = APIRouter()


@router.get("/")
def listar_cdp(db: Session = Depends(get_db)):
    registros = db.query(CDP).all()
    return jsonable_encoder(registros)


@router.post("/upload")
async def upload_cdp(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.lower().endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="El archivo debe ser Excel (.xlsx o .xls)")

    contents = await file.read()
    df = pd.read_excel(BytesIO(contents))

    # Normalizar nombres de columnas para evitar problemas de mayúsculas, espacios o caracteres especiales
    def _normalize(col_name: str) -> str:
        # quita espacios al inicio/fin, reemplaza espacios duros y pasa a minúsculas
        return str(col_name).replace("\xa0", " ").strip().lower()

    df.columns = [_normalize(c) for c in df.columns]

    # Se asume que los nombres de columnas del Excel coinciden (o son muy parecidos) a los del SQL.
    # Ajusta aquí los nombres exactos de columnas según tu archivo.
    # Usamos las versiones normalizadas (minúsculas) como claves del mapa
    column_map = {
        "numero documento": "numero_documento",
        "fecha de registro": "fecha_registro",
        "fecha de creacion": "fecha_creacion",
        "tipo de cdp": "tipo_cdp",
        "estado": "estado",
        "dependencia": "dependencia",
        "dependencia descripcion": "dependencia_descripcion",
        "rubro": "rubro",
        "descripcion": "descripcion",
        "fuente": "fuente",
        "recurso": "recurso",
        "sit": "sit",
        "valor inicial": "valor_inicial",
        "valor operaciones": "valor_operaciones",
        "valor actual": "valor_actual",
        "saldo por comprometer": "saldo_por_comprometer",
        "objeto": "objeto",
        "solicitud cdp": "solicitud_cdp",
    }

    df = df.rename(columns=column_map)

    # Algunas columnas como 'sit' pueden no venir exactamente con ese nombre en el Excel,
    # así que no la consideramos estrictamente obligatoria.
    required_cols = [c for c in column_map.values() if c not in {"sit"}]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise HTTPException(status_code=400, detail=f"Faltan columnas en el Excel: {missing}")

    records = [
        CDP(
            numero_documento=int(row.get("numero_documento")) if not pd.isna(row.get("numero_documento")) else None,
            fecha_registro=row.get("fecha_registro"),
            fecha_creacion=row.get("fecha_creacion"),
            tipo_cdp=str(row.get("tipo_cdp")) if not pd.isna(row.get("tipo_cdp")) else None,
            estado=str(row.get("estado")) if not pd.isna(row.get("estado")) else None,
            dependencia=str(row.get("dependencia")) if not pd.isna(row.get("dependencia")) else None,
            dependencia_descripcion=str(row.get("dependencia_descripcion")) if not pd.isna(row.get("dependencia_descripcion")) else None,
            rubro=str(row.get("rubro")) if not pd.isna(row.get("rubro")) else None,
            descripcion=str(row.get("descripcion")) if not pd.isna(row.get("descripcion")) else None,
            fuente=str(row.get("fuente")) if not pd.isna(row.get("fuente")) else None,
            recurso=str(row.get("recurso")) if not pd.isna(row.get("recurso")) else None,
            sit=str(row.get("sit")) if not pd.isna(row.get("sit")) else None,
            valor_inicial=row.get("valor_inicial"),
            valor_operaciones=row.get("valor_operaciones"),
            valor_actual=row.get("valor_actual"),
            saldo_por_comprometer=row.get("saldo_por_comprometer"),
            objeto=str(row.get("objeto")) if not pd.isna(row.get("objeto")) else None,
            solicitud_cdp=int(row.get("solicitud_cdp")) if not pd.isna(row.get("solicitud_cdp")) else None,
        )
        for _, row in df.iterrows()
    ]

    db.bulk_save_objects(records)
    db.commit()

    return {"insertados": len(records)}
