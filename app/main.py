from fastapi import FastAPI

from .routers import cdp, crp, eje

app = FastAPI(title="API Presupuesto")


app.include_router(cdp.router, prefix="/cdp", tags=["CDP"])
app.include_router(crp.router, prefix="/crp", tags=["CRP"])
app.include_router(eje.router, prefix="/eje", tags=["EJE"])


@app.get("/")
async def root():
    return {"message": "API Presupuesto funcionando"}
