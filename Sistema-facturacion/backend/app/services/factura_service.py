from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.factura import Factura, DetalleFactura, EstadoFactura
from app.models.cliente import Cliente
from app.schemas.factura import FacturaCreate
from fastapi import HTTPException
from decimal import Decimal
from datetime import datetime

def generate_invoice_number(db: Session) -> str:
    year = datetime.now().year
    last = db.query(Factura).filter(
        Factura.numero.like(f"FAC-{year}-%")
    ).order_by(Factura.id.desc()).first()
    
    if last:
        last_num = int(last.numero.split("-")[-1])
        next_num = last_num + 1
    else:
        next_num = 1
    
    return f"FAC-{year}-{next_num:05d}"

def create_factura(db: Session, factura_data: FacturaCreate):
    cliente = db.query(Cliente).filter(Cliente.id == factura_data.cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    subtotal = Decimal("0")
    detalles_db = []
    
    for det in factura_data.detalles:
        total_linea = det.cantidad * det.precio_unitario
        subtotal += total_linea
        detalles_db.append(DetalleFactura(
            descripcion=det.descripcion,
            cantidad=det.cantidad,
            precio_unitario=det.precio_unitario,
            total_linea=total_linea
        ))
    
    impuestos = subtotal * Decimal("0.19")
    total = subtotal + impuestos
    
    db_factura = Factura(
        numero=generate_invoice_number(db),
        cliente_id=factura_data.cliente_id,
        subtotal=subtotal,
        impuestos=impuestos,
        total=total,
        estado=EstadoFactura.ACTIVA,
        notas=factura_data.notas,
        detalles=detalles_db
    )
    
    db.add(db_factura)
    db.commit()
    db.refresh(db_factura)
    return db_factura

def get_factura(db: Session, factura_id: int):
    return db.query(Factura).filter(Factura.id == factura_id).first()

def get_facturas(db: Session, skip: int = 0, limit: int = 100, 
                 numero: str = None, cliente: str = None,
                 fecha_desde: datetime = None, fecha_hasta: datetime = None):
    query = db.query(Factura)
    
    if numero:
        query = query.filter(Factura.numero.ilike(f"%{numero}%"))
    if cliente:
        query = query.join(Cliente).filter(Cliente.nombre.ilike(f"%{cliente}%"))
    if fecha_desde:
        query = query.filter(Factura.fecha >= fecha_desde)
    if fecha_hasta:
        query = query.filter(Factura.fecha <= fecha_hasta)
    
    return query.order_by(Factura.created_at.desc()).offset(skip).limit(limit).all()

def anular_factura(db: Session, factura_id: int):
    factura = db.query(Factura).filter(Factura.id == factura_id).first()
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    if factura.estado == EstadoFactura.ANULADA:
        raise HTTPException(status_code=400, detail="La factura ya esta anulada")
    
    factura.estado = EstadoFactura.ANULADA
    db.commit()
    db.refresh(factura)
    return factura