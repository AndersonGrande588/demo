from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from app.database import Base
import enum

class RolUsuario(str, enum.Enum):
    ADMINISTRADOR = "administrador"
    EMPLEADO = "empleado"
    GERENTE = "gerente"

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    rol = Column(Enum(RolUsuario), default=RolUsuario.EMPLEADO, nullable=False)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())