let clientesData = [];
let editingClienteId = null;

document.addEventListener('DOMContentLoaded', function() {
    if (!checkAuth()) return;
    
    loadUserInfo();
    loadClientes();
    
    document.getElementById('searchClientes').addEventListener('input', debounce(searchClientes, 300));
    document.getElementById('clienteForm').addEventListener('submit', saveCliente);
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

async function loadClientes() {
    try {
        toggleLoading(true);
        clientesData = await apiRequest('/api/clientes');
        renderClientes(clientesData);
    } catch (error) {
        showAlert('Error al cargar clientes', 'error');
    } finally {
        toggleLoading(false);
    }
}

function renderClientes(clientes) {
    const tbody = document.getElementById('clientesTable');
    
    if (clientes.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;">No se encontraron clientes</td></tr>';
        return;
    }
    
    tbody.innerHTML = clientes.map(c => `
        <tr>
            <td>${escapeHtml(c.nombre)}</td>
            <td>${escapeHtml(c.documento)}</td>
            <td>${escapeHtml(c.telefono || 'N/A')}</td>
            <td>${escapeHtml(c.email || 'N/A')}</td>
            <td>${escapeHtml(c.direccion || 'N/A')}</td>
            <td>
                <button class="btn btn-sm btn-primary" onclick="editCliente(${c.id})">Editar</button>
                ${hasRole(['administrador']) ? `<button class="btn btn-sm btn-danger" onclick="deleteCliente(${c.id})">Eliminar</button>` : ''}
            </td>
        </tr>
    `).join('');
}

async function searchClientes() {
    const query = document.getElementById('searchClientes').value;
    try {
        const clientes = await apiRequest(`/api/clientes?q=${encodeURIComponent(query)}`);
        renderClientes(clientes);
    } catch (error) {
        showAlert('Error en la busqueda', 'error');
    }
}

function openModal() {
    editingClienteId = null;
    document.getElementById('clienteForm').reset();
    document.getElementById('modalTitle').textContent = 'Nuevo Cliente';
    toggleModal('clienteModal', true);
}

function closeModal() {
    toggleModal('clienteModal', false);
    console.log("close Modal onclick");    
}


function editCliente(id) {
    const cliente = clientesData.find(c => c.id === id);
    if (!cliente) return;
    
    editingClienteId = id;
    document.getElementById('nombre').value = cliente.nombre;
    document.getElementById('documento').value = cliente.documento;
    document.getElementById('telefono').value = cliente.telefono || '';
    document.getElementById('email').value = cliente.email || '';
    document.getElementById('direccion').value = cliente.direccion || '';
    document.getElementById('modalTitle').textContent = 'Editar Cliente';
    toggleModal('clienteModal', true);
}

async function saveCliente(e) {
    e.preventDefault();
    
    const data = {
        nombre: document.getElementById('nombre').value,
        documento: document.getElementById('documento').value,
        telefono: document.getElementById('telefono').value || null,
        email: document.getElementById('email').value || null,
        direccion: document.getElementById('direccion').value || null
    };
    
    try {
        toggleLoading(true);
        
        if (editingClienteId) {
            await apiRequest(`/api/clientes/${editingClienteId}`, {
                method: 'PUT',
                body: JSON.stringify(data)
            });
            showAlert('Cliente actualizado correctamente', 'success');
        } else {
            await apiRequest('/api/clientes', {
                method: 'POST',
                body: JSON.stringify(data)
            });
            showAlert('Cliente creado correctamente', 'success');
        }
        
        toggleModal('clienteModal', false);
        loadClientes();
        
    } catch (error) {
        showAlert(error.message, 'error');
    } finally {
        toggleLoading(false);
    }
}

async function deleteCliente(id) {
    if (!confirm('Esta seguro de eliminar este cliente?')) return;
    
    try {
        await apiRequest(`/api/clientes/${id}`, { method: 'DELETE' });
        showAlert('Cliente eliminado correctamente', 'success');
        loadClientes();
    } catch (error) {
        showAlert(error.message, 'error');
    }
}