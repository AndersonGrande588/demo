from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from decimal import Decimal
from app.models.factura import EstadoFactura
from app.schemas.cliente import ClienteResponse

class DetalleFacturaBase(BaseModel):
    descripcion: str
    cantidad: Decimal = Field(gt=0)
    precio_unitario: Decimal = Field(gt=0)

class DetalleFacturaCreate(DetalleFacturaBase):
    pass

class DetalleFacturaResponse(DetalleFacturaBase):
    id: int
    total_linea: Decimal
    
    class Config:
        from_attributes = True

class FacturaBase(BaseModel):
    cliente_id: int
    notas: Optional[str] = None

class FacturaCreate(FacturaBase):
    detalles: List[DetalleFacturaCreate]

class FacturaUpdate(BaseModel):
    notas: Optional[str] = None

class FacturaResponse(BaseModel):
    id: int
    numero: str
    cliente_id: int
    cliente: ClienteResponse
    fecha: datetime
    subtotal: Decimal
    impuestos: Decimal
    total: Decimal
    estado: EstadoFactura
    notas: Optional[str]
    detalles: List[DetalleFacturaResponse]
    created_at: datetime
    
    class Config:
        from_attributes = True

class FacturaBusqueda(BaseModel):
    numero: Optional[str] = None
    cliente: Optional[str] = None
    fecha_desde: Optional[datetime] = None
    fecha_hasta: Optional[datetime] = None