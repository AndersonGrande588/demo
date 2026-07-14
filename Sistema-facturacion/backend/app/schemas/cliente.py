from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ClienteBase(BaseModel):
    nombre: str
    documento: str
    telefono: Optional[str] = None
    email: Optional[str] = None
    direccion: Optional[str] = None

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    documento: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    direccion: Optional[str] = None

class ClienteResponse(ClienteBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True