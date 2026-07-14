from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class EstadoFactura(str, enum.Enum):
    ACTIVA = "activa"
    ANULADA = "anulada"

class Factura(Base):
    __tablename__ = "facturas"
    
    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String(20), unique=True, nullable=False, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    fecha = Column(DateTime(timezone=True), server_default=func.now())
    subtotal = Column(Numeric(12, 2), nullable=False)
    impuestos = Column(Numeric(12, 2), default=0)
    total = Column(Numeric(12, 2), nullable=False)
    estado = Column(Enum(EstadoFactura), default=EstadoFactura.ACTIVA)
    notas = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    cliente = relationship("Cliente", back_populates="facturas")
    detalles = relationship("DetalleFactura", back_populates="factura", cascade="all, delete-orphan")

class DetalleFactura(Base):
    __tablename__ = "detalle_facturas"
    
    id = Column(Integer, primary_key=True, index=True)
    factura_id = Column(Integer, ForeignKey("facturas.id"), nullable=False)
    descripcion = Column(String(255), nullable=False)
    cantidad = Column(Numeric(10, 2), nullable=False)
    precio_unitario = Column(Numeric(12, 2), nullable=False)
    total_linea = Column(Numeric(12, 2), nullable=False)
    
    factura = relationship("Factura", back_populates="detalles")

from app.models.cliente import Cliente
Cliente.facturas = relationship("Factura", back_populates="cliente")