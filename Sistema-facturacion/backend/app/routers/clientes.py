from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse
from app.models.cliente import Cliente
from app.models.usuario import Usuario, RolUsuario
from app.utils.security import get_current_user, require_role

router = APIRouter(prefix="/api/clientes", tags=["Clientes"])

@router.get("/", response_model=List[ClienteResponse])
def buscar_clientes(
    q: str = "",
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    query = db.query(Cliente)
    if q:
        query = query.filter(
            (Cliente.nombre.ilike(f"%{q}%")) | 
            (Cliente.documento.ilike(f"%{q}%"))
        )
    return query.offset(skip).limit(limit).all()

@router.post("/", response_model=ClienteResponse, status_code=201)
def crear_cliente(
    cliente: ClienteCreate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(
        RolUsuario.ADMINISTRADOR.value, 
        RolUsuario.EMPLEADO.value
    ))
):
    existing = db.query(Cliente).filter(Cliente.documento == cliente.documento).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ya existe un cliente con ese documento")
    
    db_cliente = Cliente(**cliente.dict())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

@router.get("/{cliente_id}", response_model=ClienteResponse)
def obtener_cliente(
    cliente_id: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@router.put("/{cliente_id}", response_model=ClienteResponse)
def actualizar_cliente(
    cliente_id: int, 
    cliente: ClienteUpdate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(
        RolUsuario.ADMINISTRADOR.value, 
        RolUsuario.EMPLEADO.value
    ))
):
    db_cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    update_data = cliente.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_cliente, field, value)
    
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

@router.delete("/{cliente_id}")
def eliminar_cliente(
    cliente_id: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(RolUsuario.ADMINISTRADOR.value))
):
    db_cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    db.delete(db_cliente)
    db.commit()
    return {"message": "Cliente eliminado correctamente"}