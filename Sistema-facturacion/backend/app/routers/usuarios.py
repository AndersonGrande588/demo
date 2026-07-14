from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.usuario import UsuarioResponse, UsuarioCreate, UsuarioUpdate
from app.services.auth_service import get_users, get_user_by_id, update_user, delete_user, create_user
from app.utils.security import get_current_user, require_role
from app.models.usuario import Usuario, RolUsuario

router = APIRouter(prefix="/api/usuarios", tags=["Usuarios"])

@router.get("/", response_model=List[UsuarioResponse])
def listar_usuarios(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(RolUsuario.ADMINISTRADOR.value))
):
    return get_users(db, skip=skip, limit=limit)

@router.post("/", response_model=UsuarioResponse, status_code=201)
def crear_usuario(
    user: UsuarioCreate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(RolUsuario.ADMINISTRADOR.value))
):
    return create_user(db, user)

@router.get("/{user_id}", response_model=UsuarioResponse)
def obtener_usuario(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(RolUsuario.ADMINISTRADOR.value))
):
    return get_user_by_id(db, user_id)

@router.put("/{user_id}", response_model=UsuarioResponse)
def actualizar_usuario(
    user_id: int, 
    user: UsuarioUpdate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(RolUsuario.ADMINISTRADOR.value))
):
    return update_user(db, user_id, user)

@router.delete("/{user_id}")
def eliminar_usuario(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(RolUsuario.ADMINISTRADOR.value))
):
    delete_user(db, user_id)
    return {"message": "Usuario desactivado correctamente"}