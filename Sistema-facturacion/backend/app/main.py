from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth, usuarios, clientes, facturas
from app.services.auth_service import init_admin_user
from app.database import SessionLocal

Base.metadata.create_all(bind=engine)

with SessionLocal() as db:
    init_admin_user(db)

app = FastAPI(
    title="Sistema Web de Facturacion - Hayabuza",
    description="API para gestion de facturas de Jose Automotriz",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(clientes.router)
app.include_router(facturas.router)

@app.get("/")
def root():
    return {
        "message": "Sistema Web de Facturacion - Hayabuza",
        "version": "1.0.0",
        "autor": "Anderson Grande"
    }

@app.get("/api/health")
def health_check():
    return {"status": "ok"}