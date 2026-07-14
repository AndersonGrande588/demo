let facturasData = [];
let clientesList = [];

document.addEventListener('DOMContentLoaded', function() {
    if (!checkAuth()) return;
    
    loadUserInfo();
    loadFacturas();
    loadClientesSelect();
    
    document.getElementById('searchFacturas').addEventListener('input', debounce(searchFacturas, 300));
});

function loadUserInfo() {
    const user = getUser();
    if (user) {
        document.getElementById('userName').textContent = user.nombre;
        document.getElementById('userRole').textContent = user.rol;
    }
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

async function loadFacturas() {
    try {
        toggleLoading(true);
        facturasData = await apiRequest('/api/facturas');
        renderFacturas(facturasData);
    } catch (error) {
        showAlert('Error al cargar facturas', 'error');
    } finally {
        toggleLoading(false);
    }
}

function renderFacturas(facturas) {
    const tbody = document.getElementById('facturasTable');
    
    if (facturas.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;">No se encontraron facturas</td></tr>';
        return;
    }
    
    tbody.innerHTML = facturas.map(f => `
        <tr>
            <td>${f.numero}</td>
            <td>${escapeHtml(f.cliente.nombre)}</td>
            <td>${formatDate(f.fecha)}</td>
            <td>${formatCurrency(f.total)}</td>
            <td><span class="badge badge-${f.estado === 'activa' ? 'success' : 'danger'}">${f.estado}</span></td>
            <td>${f.detalles.length} items</td>
            <td>
                <a href="ver-factura.html?id=${f.id}" class="btn btn-sm btn-primary">Ver</a>
                <a href="${API_URL}/api/facturas/${f.id}/pdf" target="_blank" class="btn btn-sm btn-secondary">PDF</a>
                ${hasRole(['administrador']) && f.estado === 'activa' ? `<button class="btn btn-sm btn-danger" onclick="anularFactura(${f.id})">Anular</button>` : ''}
            </td>
        </tr>
    `).join('');
}

async function searchFacturas() {
    const query = document.getElementById('searchFacturas').value;
    try {
        const facturas = await apiRequest(`/api/facturas?cliente=${encodeURIComponent(query)}`);
        renderFacturas(facturas);
    } catch (error) {
        showAlert('Error en la busqueda', 'error');
    }
}

async function loadClientesSelect() {
    try {
        clientesList = await apiRequest('/api/clientes');
        const selects = document.querySelectorAll('.cliente-select');
        selects.forEach(select => {
            select.innerHTML = '<option value="">Seleccione un cliente</option>' +
                clientesList.map(c => `<option value="${c.id}">${escapeHtml(c.nombre)} - ${escapeHtml(c.documento)}</option>`).join('');
        });
    } catch (error) {
        console.error('Error cargando clientes:', error);
    }
}

async function anularFactura(id) {
    if (!confirm('Esta seguro de anular esta factura?')) return;
    
    try {
        await apiRequest(`/api/facturas/${id}/anular`, { method: 'PUT' });
        showAlert('Factura anulada correctamente', 'success');
        loadFacturas();
    } catch (error) {
        showAlert(error.message, 'error');
    }
}

// Para nueva-factura.html
let itemCount = 0;

function addItem() {
    itemCount++;
    const container = document.getElementById('itemsContainer');
    const row = document.createElement('div');
    row.className = 'item-row';
    row.id = `item-${itemCount}`;
    row.innerHTML = `
        <input type="text" placeholder="Descripcion" class="item-desc" required>
        <input type="number" placeholder="Cantidad" class="item-qty" min="0.01" step="0.01" required onchange="calculateTotals()">
        <input type="number" placeholder="Precio" class="item-price" min="0.01" step="0.01" required onchange="calculateTotals()">
        <span class="item-total">$0.00</span>
        <button type="button" class="btn btn-sm btn-danger" onclick="removeItem(${itemCount})">X</button>
    `;
    container.appendChild(row);
}

function removeItem(id) {
    const row = document.getElementById(`item-${id}`);
    if (row) row.remove();
    calculateTotals();
}

function calculateTotals() {
    let subtotal = 0;
    document.querySelectorAll('.item-row').forEach(row => {
        const qty = parseFloat(row.querySelector('.item-qty').value) || 0;
        const price = parseFloat(row.querySelector('.item-price').value) || 0;
        const total = qty * price;
        row.querySelector('.item-total').textContent = formatCurrency(total);
        subtotal += total;
    });
    
    const impuestos = subtotal * 0.19;
    const total = subtotal + impuestos;
    
    document.getElementById('subtotal').textContent = formatCurrency(subtotal);
    document.getElementById('impuestos').textContent = formatCurrency(impuestos);
    document.getElementById('total').textContent = formatCurrency(total);
}

async function saveFactura(e) {
    e.preventDefault();
    
    const clienteId = document.getElementById('clienteSelect').value;
    if (!clienteId) {        return;
    }
    
    try {
        toggleLoading(true);
        const factura = await apiRequest(`/api/facturas/${id}`);
        renderFacturaDetalle(factura);
    } catch (error) {
        showAlert(error.message, 'error');
    } finally {
        toggleLoading(false);
    }
}

function renderFacturaDetalle(factura) {
    document.getElementById('facturaNumero').textContent = factura.numero;
    document.getElementById('facturaEstado').innerHTML = 
        `<span class="badge badge-${factura.estado === 'activa' ? 'success' : 'danger'}">${factura.estado.toUpperCase()}</span>`;
    
    document.getElementById('clienteNombre').textContent = factura.cliente.nombre;
    document.getElementById('clienteDocumento').textContent = factura.cliente.documento;
    document.getElementById('clienteTelefono').textContent = factura.cliente.telefono || 'N/A';
    document.getElementById('clienteEmail').textContent = factura.cliente.email || 'N/A';
    document.getElementById('clienteDireccion').textContent = factura.cliente.direccion || 'N/A';
    
    document.getElementById('facturaFecha').textContent = formatDate(factura.fecha);
    document.getElementById('facturaNotas').textContent = factura.notas || 'Sin notas';
    
    const tbody = document.getElementById('detalleItems');
    tbody.innerHTML = factura.detalles.map(d => `
        <tr>
            <td>${escapeHtml(d.descripcion)}</td>
            <td>${d.cantidad}</td>
            <td>${formatCurrency(d.precio_unitario)}</td>
            <td>${formatCurrency(d.total_linea)}</td>
        </tr>
    `).join('');
    
    document.getElementById('subtotalDisplay').textContent = formatCurrency(factura.subtotal);
    document.getElementById('impuestosDisplay').textContent = formatCurrency(factura.impuestos);
    document.getElementById('totalDisplay').textContent = formatCurrency(factura.total);
    
    // Configurar botón de descarga
    document.getElementById('btnDescargar').onclick = () => {
        window.open(`${API_URL}/api/facturas/${factura.id}/pdf`, '_blank');
    };
    
    // Mostrar botón anular solo para admin y facturas activas
    const btnAnular = document.getElementById('btnAnular');
    if (hasRole(['administrador']) && factura.estado === 'activa') {
        btnAnular.style.display = 'inline-block';
        btnAnular.onclick = async () => {
            if (!confirm('¿Esta seguro de anular esta factura?')) return;
            try {
                await apiRequest(`/api/facturas/${factura.id}/anular`, { method: 'PUT' });
                showAlert('Factura anulada correctamente', 'success');
                setTimeout(() => location.reload(), 1000);
            } catch (error) {
                showAlert(error.message, 'error');
            }
        };
    } else {
        btnAnular.style.display = 'none';
    }
}

function loadUserInfo() {
    const user = getUser();
    if (user) {
        const elName = document.getElementById('userName');
        const elRole = document.getElementById('userRole');
        if (elName) elName.textContent = user.nombre;
        if (elRole) elRole.textContent = user.rol;
    }
}

function setupSidebar() {
    const user = getUser();
    const adminOnly = document.querySelectorAll('.admin-only');
    if (user && user.rol !== 'administrador') {
        adminOnly.forEach(el => el.style.display = 'none');
    }
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}