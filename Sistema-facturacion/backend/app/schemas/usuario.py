from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.models.usuario import RolUsuario

class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr
    rol: RolUsuario = RolUsuario.EMPLEADO
    activo: bool = True

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    rol: Optional[RolUsuario] = None
    activo: Optional[bool] = None
    password: Optional[str] = None

class UsuarioResponse(UsuarioBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioResponse