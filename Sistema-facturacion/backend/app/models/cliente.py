from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base

class Cliente(Base):
    __tablename__ = "clientes"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    documento = Column(String(50), unique=True, nullable=False, index=True)
    telefono = Column(String(20))
    email = Column(String(100))
    direccion = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())