document.addEventListener('DOMContentLoaded', function() {
    if (!checkAuth()) return;
    
    loadUserInfo();
    loadStats();
    loadRecentInvoices();
});

function loadUserInfo() {
    const user = getUser();
    if (user) {
        document.getElementById('userName').textContent = user.nombre;
        document.getElementById('userRole').textContent = user.rol;
    }
}

async function loadStats() {
    try {
        const facturas = await apiRequest('/api/facturas?limit=9999');
        const clientes = await apiRequest('/api/clientes?limit=9999');
        
        const totalFacturas = facturas.length;
        const totalClientes = clientes.length;
        const totalVentas = facturas.reduce((sum, f) => sum + parseFloat(f.total), 0);
        const facturasActivas = facturas.filter(f => f.estado === 'activa').length;
        
        document.getElementById('statFacturas').textContent = totalFacturas;
        document.getElementById('statClientes').textContent = totalClientes;
        document.getElementById('statVentas').textContent = formatCurrency(totalVentas);
        document.getElementById('statActivas').textContent = facturasActivas;
        
    } catch (error) {
        console.error('Error cargando estadisticas:', error);
    }
}

async function loadRecentInvoices() {
    try {
        const facturas = await apiRequest('/api/facturas?limit=5');
        const tbody = document.getElementById('recentInvoices');
        
        if (facturas.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;">No hay facturas registradas</td></tr>';
            return;
        }
        
        tbody.innerHTML = facturas.map(f => `
            <tr>
                <td>${f.numero}</td>
                <td>${f.cliente.nombre}</td>
                <td>${formatDate(f.fecha)}</td>
                <td>${formatCurrency(f.total)}</td>
                <td><span class="badge badge-${f.estado === 'activa' ? 'success' : 'danger'}">${f.estado}</span></td>
            </tr>
        `).join('');
        
    } catch (error) {
        console.error('Error cargando facturas recientes:', error);
    }
}