from app.models.factura import Factura
from datetime import datetime

def generate_invoice_pdf(factura: Factura) -> bytes:
    """
    Genera un HTML de la factura que el navegador puede imprimir a PDF.
    Retorna bytes UTF-8 del HTML.
    """
    items_html = ""
    for det in factura.detalles:
        items_html += f"""
        <tr>
            <td>{det.descripcion}</td>
            <td style="text-align:center;">{float(det.cantidad):.2f}</td>
            <td style="text-align:right;">${float(det.precio_unitario):,.2f}</td>
            <td style="text-align:right;">${float(det.total_linea):,.2f}</td>
        </tr>
        """
    
    estado_class = "anulada" if factura.estado.value == "anulada" else ""
    anulada_banner = ""
    if factura.estado.value == "anulada":
        anulada_banner = '<div class="anulada">FACTURA ANULADA</div>'
    
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Factura {factura.numero}</title>
    <style>
        @page {{ size: A4; margin: 2cm; }}
        body {{ font-family: Arial, sans-serif; font-size: 13px; color: #333; margin: 0; padding: 20px; }}
        .header {{ text-align: center; border-bottom: 3px solid #1a5276; padding-bottom: 15px; margin-bottom: 20px; }}
        .header h1 {{ color: #1a5276; margin: 0; font-size: 28px; }}
        .header p {{ margin: 5px 0; color: #666; font-size: 13px; }}
        .info-box {{ background: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 15px; }}
        .info-box h3 {{ color: #1a5276; margin: 0 0 10px 0; font-size: 15px; }}
        .info-box p {{ margin: 4px 0; }}
        .flex {{ display: flex; justify-content: space-between; gap: 20px; }}
        .flex > div {{ flex: 1; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th {{ background: #1a5276; color: white; padding: 12px; text-align: left; font-size: 13px; }}
        td {{ padding: 10px 12px; border-bottom: 1px solid #ddd; }}
        tr:nth-child(even) {{ background: #f8f9fa; }}
        .totals {{ width: 300px; margin-left: auto; margin-top: 20px; }}
        .totals .row {{ display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #ddd; }}
        .totals .total {{ font-size: 18px; font-weight: bold; color: #1a5276; border-top: 2px solid #1a5276; border-bottom: none; padding-top: 12px; margin-top: 5px; }}
        .footer {{ margin-top: 40px; text-align: center; color: #888; font-size: 11px; border-top: 1px solid #ddd; padding-top: 15px; }}
        .anulada {{ color: #e74c3c; font-weight: bold; font-size: 22px; text-align: center; margin: 20px 0; border: 4px solid #e74c3c; padding: 15px; }}
        @media print {{ .no-print {{ display: none; }} body {{ padding: 0; }} }}
    </style>
</head>
<body>
    <div class="header">
        <h1>HAYABUZA</h1>
        <p>Sistema de Facturacion</p>
        <p>Cliente: Jose Automotriz</p>
    </div>
    
    {anulada_banner}
    
    <div class="flex">
        <div class="info-box">
            <h3>Facturar a:</h3>
            <p><strong>{factura.cliente.nombre}</strong></p>
            <p>Documento: {factura.cliente.documento}</p>
            <p>Telefono: {factura.cliente.telefono or 'N/A'}</p>
            <p>Email: {factura.cliente.email or 'N/A'}</p>
            <p>Direccion: {factura.cliente.direccion or 'N/A'}</p>
        </div>
        <div class="info-box">
            <h3>Informacion de la Factura</h3>
            <p><strong>Numero:</strong> {factura.numero}</p>
            <p><strong>Fecha:</strong> {factura.fecha.strftime('%d/%m/%Y %H:%M')}</p>
            <p><strong>Estado:</strong> {factura.estado.value.upper()}</p>
        </div>
    </div>
    
    <table>
        <thead>
            <tr>
                <th>Descripcion</th>
                <th style="text-align:center;">Cantidad</th>
                <th style="text-align:right;">Precio Unit.</th>
                <th style="text-align:right;">Total</th>
            </tr>
        </thead>
        <tbody>
            {items_html}
        </tbody>
    </table>
    
    <div class="totals">
        <div class="row">
            <span>Subtotal:</span>
            <span>${float(factura.subtotal):,.2f}</span>
        </div>
        <div class="row">
            <span>Impuestos (19%):</span>
            <span>${float(factura.impuestos):,.2f}</span>
        </div>
        <div class="row total">
            <span>TOTAL:</span>
            <span>${float(factura.total):,.2f}</span>
        </div>
    </div>
    
    {f'<div style="margin-top:20px;padding:10px;background:#f8f9fa;border-radius:5px;"><strong>Notas:</strong> {factura.notas}</div>' if factura.notas else ''}
    
    <div class="footer">
        <p>Documento generado el {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
        <p>Sistema Web de Facturacion - Hayabuza &copy; 2026</p>
    </div>
    
    <div class="no-print" style="margin-top:30px;text-align:center;">
        <button onclick="window.print()" style="padding:12px 30px;font-size:16px;background:#1a5276;color:white;border:none;border-radius:5px;cursor:pointer;">Imprimir / Guardar como PDF</button>
    </div>
</body>
</html>"""
    
    return html.encode('utf-8')