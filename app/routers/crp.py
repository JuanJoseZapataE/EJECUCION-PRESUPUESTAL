from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Form
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
import pandas as pd
from io import BytesIO
from datetime import date

from app.database import get_db
from app.models import CRP

router = APIRouter()


@router.get("/")
def listar_crp(db: Session = Depends(get_db)):
    registros = db.query(CRP).all()
    return jsonable_encoder(registros)


@router.post("/upload")
async def upload_crp(
    fecha_corte: date | None = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not file.filename.lower().endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="El archivo debe ser Excel (.xlsx o .xls)")

    contents = await file.read()
    df = pd.read_excel(BytesIO(contents))

    # Normalizar nombres de columnas para evitar problemas de mayúsculas, espacios o caracteres especiales
    def _normalize(col_name: str) -> str:
        return str(col_name).replace("\xa0", " ").strip().lower()

    df.columns = [_normalize(c) for c in df.columns]

    column_map = {
        "numero documento": "numero_documento",
        "fecha de registro": "fecha_registro",
        "fecha de creacion": "fecha_creacion",
        "estado": "estado",
        "dependencia": "dependencia",
        "dependencia descripcion": "dependencia_descripcion",
        "rubro": "rubro",
        "descripcion": "descripcion",
        "fuente": "fuente",
        "recurso": "recurso",
        "situacion": "situacion",
        "valor inicial": "valor_inicial",
        "valor operaciones": "valor_operaciones",
        "valor actual": "valor_actual",
        "saldo por utilizar": "saldo_por_utilizar",
        "tipo identificacion": "tipo_identificacion",
        "identificacion": "identificacion",
        "nombre razon social": "nombre_razon_social",
        "medio de pago": "medio_de_pago",
        "tipo cuenta": "tipo_cuenta",
        "numero cuenta": "numero_cuenta",
        "estado cuenta": "estado_cuenta",
        "entidad nit": "entidad_nit",
        "entidad descripcion": "entidad_descripcion",
        "solicitud cdp": "solicitud_cdp",
        "cdp": "cdp",
        "compromisos": "compromisos",
        "cuentas por pagar": "cuentas_por_pagar",
        "obligaciones": "obligaciones",
        "ordenes de pago": "ordenes_de_pago",
        "reintegros": "reintegros",
        "fecha documento soporte": "fecha_documento_soporte",
        "tipo documento soporte": "tipo_documento_soporte",
        "numero documento soporte": "numero_documento_soporte",
        "observaciones": "observaciones",
    }

    df = df.rename(columns=column_map)

    required_cols = list(column_map.values())
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise HTTPException(status_code=400, detail=f"Faltan columnas en el Excel: {missing}")

    # Reemplazar NaN por None para que SQLAlchemy/MySQL acepten los valores nulos
    def _nan_to_none(value):
        return None if pd.isna(value) else value

    records = []
    for _, row in df.iterrows():
        data = {col: _nan_to_none(row.get(col)) for col in required_cols}
        data["fecha_corte"] = fecha_corte
        records.append(CRP(**data))

    db.bulk_save_objects(records)
    db.commit()

    return {"insertados": len(records)}
