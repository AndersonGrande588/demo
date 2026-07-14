from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.database import get_db
from app.schemas.factura import FacturaCreate, FacturaResponse, FacturaBusqueda
from app.services.factura_service import create_factura, get_factura, get_facturas, anular_factura
from app.services.pdf_generator import generate_invoice_pdf
from app.models.usuario import Usuario, RolUsuario
from app.utils.security import get_current_user, require_role

router = APIRouter(prefix="/api/facturas", tags=["Facturas"])

@router.get("/", response_model=List[FacturaResponse])
def buscar_facturas(
    numero: Optional[str] = None,
    cliente: Optional[str] = None,
    fecha_desde: Optional[datetime] = None,
    fecha_hasta: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return get_facturas(db, skip=skip, limit=limit, 
                       numero=numero, cliente=cliente,
                       fecha_desde=fecha_desde, fecha_hasta=fecha_hasta)

@router.post("/", response_model=FacturaResponse, status_code=201)
def crear_factura_endpoint(
    factura: FacturaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(
        RolUsuario.ADMINISTRADOR.value,
        RolUsuario.EMPLEADO.value
    ))
):
    return create_factura(db, factura)

@router.get("/{factura_id}", response_model=FacturaResponse)
def obtener_factura(
    factura_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    factura = get_factura(db, factura_id)
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return factura

@router.get("/{factura_id}/pdf")
def descargar_pdf(
    factura_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    factura = get_factura(db, factura_id)
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    
    pdf_bytes = generate_invoice_pdf(factura)
    
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={factura.numero}.pdf"
        }
    )

@router.put("/{factura_id}/anular")
def anular_factura_endpoint(
    factura_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(RolUsuario.ADMINISTRADOR.value))
):
    return anular_factura(db, factura_id)