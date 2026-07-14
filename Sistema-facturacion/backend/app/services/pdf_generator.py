from jinja2 import Template
from weasyprint import HTML
from app.models.factura import Factura
from datetime import datetime

FACTURA_HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @page { size: A4; margin: 2cm; }
        body { font-family: Arial, sans-serif; font-size: 12px; color: #333; }
        .header { text-align: center; border-bottom: 2px solid #1a5276; padding-bottom: 15px; margin-bottom: 20px; }
        .header h1 { color: #1a5276; margin: 0; font-size: 24px; }
        .header p { margin: 5px 0; color: #666; }
        .info-section { display: flex; justify-content: space-between; margin-bottom: 20px; }
        .info-box { width: 48%; }
        .info-box h3 { color: #1a5276; border-bottom: 1px solid #ddd; padding-bottom: 5px; margin-bottom: 10px; }
        .info-box p { margin: 3px 0; }
        .factura-info { background: #f8f9fa; padding: 10px; border-radius: 5px; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th { background: #1a5276; color: white; padding: 10px; text-align: left; }
        td { padding: 8px 10px; border-bottom: 1px solid #ddd; }
        tr:nth-child(even) { background: #f8f9fa; }
        .totals { width: 300px; margin-left: auto; margin-top: 20px; }
        .totals table { width: 100%; }
        .totals td { border: none; padding: 8px; }
        .totals .total-row { font-size: 16px; font-weight: bold; background: #1a5276; color: white; }
        .footer { margin-top: 40px; text-align: center; color: #666; font-size: 10px; border-top: 1px solid #ddd; padding-top: 15px; }
        .estado-anulada { color: #e74c3c; font-weight: bold; font-size: 18px; text-align: center; margin: 20px 0; border: 3px solid #e74c3c; padding: 10px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>HAYABUZA</h1>
        <p>Sistema de Facturacion</p>
        <p>Cliente: Jose Automotriz</p>
    </div>
    
    {% if factura.estado.value == 'anulada' %}
    <div class="estado-anulada">FACTURA ANULADA</div>
    {% endif %}
    
    <div class="info-section">
        <div class="info-box">
            <h3>Facturar a:</h3>
            <p><strong>{{ factura.cliente.nombre }}</strong></p>
            <p>Documento: {{ factura.cliente.documento }}</p>
            <p>Telefono: {{ factura.cliente.telefono or 'N/A' }}</p>
            <p>Email: {{ factura.cliente.email or 'N/A' }}</p>
            <p>Direccion: {{ factura.cliente.direccion or 'N/A' }}</p>
        </div>
        <div class="info-box factura-info">
            <h3>Informacion de la Factura</h3>
            <p><strong>Numero:</strong> {{ factura.numero }}</p>
            <p><strong>Fecha:</strong> {{ factura.fecha.strftime('%d/%m/%Y %H:%M') }}</p>
            <p><strong>Estado:</strong> {{ factura.estado.value.upper() }}</p>
        </div>
    </div>
    
    <table>
        <thead>
            <tr>
                <th style="width: 50%;">Descripcion</th>
                <th style="width: 15%;">Cantidad</th>
                <th style="width: 20%;">Precio Unit.</th>
                <th style="width: 15%;">Total</th>
            </tr>
        </thead>
        <tbody>
            {% for detalle in factura.detalles %}
            <tr>
                <td>{{ detalle.descripcion }}</td>
                <td>{{ "%.2f"|format(detalle.cantidad) }}</td>
                <td>${{ "%.2f"|format(detalle.precio_unitario) }}</td>
                <td>${{ "%.2f"|format(detalle.total_linea) }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    
    <div class="totals">
        <table>
            <tr>
                <td><strong>Subtotal:</strong></td>
                <td style="text-align: right;">${{ "%.2f"|format(factura.subtotal) }}</td>
            </tr>
            <tr>
                <td><strong>Impuestos (19%):</strong></td>
                <td style="text-align: right;">${{ "%.2f"|format(factura.impuestos) }}</td>
            </tr>
            <tr class="total-row">
                <td><strong>TOTAL:</strong></td>
                <td style="text-align: right;"><strong>${{ "%.2f"|format(factura.total) }}</strong></td>
            </tr>
        </table>
    </div>
    
    {% if factura.notas %}
    <div style="margin-top: 30px; padding: 10px; background: #f8f9fa; border-radius: 5px;">
        <strong>Notas:</strong> {{ factura.notas }}
    </div>
    {% endif %}
    
    <div class="footer">
        <p>Documento generado el {{ now.strftime('%d/%m/%Y %H:%M:%S') }}</p>
        <p>Sistema Web de Facturacion - Hayabuza 2026</p>
    </div>
</body>
</html>
"""

def generate_invoice_pdf(factura: Factura) -> bytes:
    template = Template(FACTURA_HTML_TEMPLATE)
    html_content = template.render(factura=factura, now=datetime.now())
    
    pdf = HTML(string=html_content).write_pdf()
    return pdf