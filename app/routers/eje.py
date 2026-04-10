from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
import pandas as pd
from io import BytesIO

from app.database import get_db
from app.models import Eje

router = APIRouter()


@router.get("/")
def listar_eje(db: Session = Depends(get_db)):
    registros = db.query(Eje).all()
    return jsonable_encoder(registros)


@router.post("/upload")
async def upload_eje(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.lower().endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="El archivo debe ser Excel (.xlsx o .xls)")

    contents = await file.read()
    # Leemos sin encabezados porque hay filas iniciales y múltiples bloques
    df = pd.read_excel(BytesIO(contents), header=None)

    def _normalize(value) -> str:
        return str(value).replace("\xa0", " ").strip().lower() if not pd.isna(value) else ""

    # Mapeo de nombres de columna (normalizados) a campos del modelo
    header_name_map = {
        "tipo": "tipo",
        "cta": "cta",
        "subc": "subc",
        "objg": "objg",
        "ord": "ord",
        "sord": "sord",
        "item": "item",
        "sitem": "sitem",
        "concepto": "concepto",
        "fuente": "fuente",
        "situacion": "situacion",
        "rec": "rec",
        "recurso": "recurso",
        "apropiacion vigente dep.gsto.": "apropiacion_vigente_dep_gsto",
        "total cdp dep.gstos": "total_cdp_dep_gstos",
        "apropiacion disponible dep.gsto.": "apropiacion_disponible_dep_gsto",
        "total cdp modificacion dep.gstos": "total_cdp_modificacion_dep_gstos",
        "total compromiso dep.gstos": "total_compromiso_dep_gstos",
        "cdp por comprometer dep.gstos": "cdp_por_comprometer_dep_gstos",
        "total obligaciones dep.gstos": "total_obligaciones_dep_gstos",
        "compromiso por obligar dep.gstos": "compromiso_por_obligar_dep_gstos",
        "total ordenes de pago dep.gstos": "total_ordenes_pago_dep_gstos",
        "obligaciones por ordenar dep.gstos": "obligaciones_por_ordenar_dep_gstos",
        "pagos dep.gstos": "pagos_dep_gstos",
        "ordenes de pago por pagar dep.gstos": "ordenes_pago_por_pagar_dep_gstos",
        "total reintegros dep.gstos": "total_reintegros_dep_gstos",
    }

    def _nan_to_none(v):
        return None if pd.isna(v) else v

    records = []
    current_dep = None  # dependencia_de_afectacion_de_gastos actual
    current_cols = None  # mapeo: campo -> índice de columna

    for idx, row in df.iterrows():
        norm_row = [_normalize(v) for v in row]

        # Fila de título de bloque (dependencia de afectación de gastos)
        if norm_row and "dependencia de afectacion de gastos" in norm_row[0]:
            # Usamos el valor original completo como título
            current_dep = str(row.iloc[0]).replace("\xa0", " ").strip()
            current_cols = None
            continue

        # Fila de encabezados de bloque (donde aparecen TIPO, CTA, etc.)
        if any(n in header_name_map for n in norm_row):
            col_map = {}
            for col_idx, name in enumerate(norm_row):
                if name in header_name_map:
                    field = header_name_map[name]
                    col_map[field] = col_idx
            # Requerimos al menos un subconjunto razonable para considerar que es encabezado
            if {"tipo", "cta", "subc"}.issubset(col_map.keys()):
                current_cols = col_map
            continue

        # Filas de datos: solo si ya tenemos una dependencia y un encabezado definido
        if current_dep and current_cols:
            # Fila vacía -> probable separación entre bloques
            if all((val is None or (isinstance(val, float) and pd.isna(val)) or str(val).strip() == "") for val in row):
                continue

            data = {
                "dependecia_de_afectacion_de_gastos": current_dep,
            }
            for field, col_idx in current_cols.items():
                value = row.iloc[col_idx] if col_idx < len(row) else None
                data[field] = _nan_to_none(value)

            records.append(Eje(**data))

    if not records:
        raise HTTPException(status_code=400, detail="No se encontraron filas válidas en el Excel de EJE")

    db.bulk_save_objects(records)
    db.commit()

    return {"insertados": len(records)}
