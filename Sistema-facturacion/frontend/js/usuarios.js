let usuariosData = [];
let editingId = null;

document.addEventListener('DOMContentLoaded', function() {
    if (!checkAuth()) return;
    
    loadUserInfo();
    setupSidebar();
    loadUsuarios();
    
    document.getElementById('usuarioForm').addEventListener('submit', saveUsuario);
});

function loadUserInfo() {
    const user = getUser();
    if (user) {
        document.getElementById('userName').textContent = user.nombre;
        document.getElementById('userRole').textContent = user.rol;
    }
}

function setupSidebar() {
    const user = getUser();
    const adminOnly = document.querySelectorAll('.admin-only');
    if (user && user.rol !== 'administrador') {
        adminOnly.forEach(el => el.style.display = 'none');
        // Redirigir si no es admin
        window.location.href = 'dashboard.html';
    }
}

async function loadUsuarios() {
    try {
        toggleLoading(true);
        usuariosData = await apiRequest('/api/usuarios');
        renderUsuarios(usuariosData);
    } catch (error) {
        showAlert(error.message, 'error');
    } finally {
        toggleLoading(false);
    }
}

function renderUsuarios(usuarios) {
    const tbody = document.getElementById('usuariosTable');
    
    if (usuarios.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;">No hay usuarios registrados</td></tr>';
        return;
    }
    
    tbody.innerHTML = usuarios.map(u => `
        <tr>
            <td>${escapeHtml(u.nombre)}</td>
            <td>${escapeHtml(u.email)}</td>
            <td><span class="badge badge-info">${u.rol}</span></td>
            <td><span class="badge badge-${u.activo ? 'success' : 'danger'}">${u.activo ? 'Activo' : 'Inactivo'}</span></td>
            <td>
                <button class="btn btn-sm btn-primary" onclick="editUsuario(${u.id})">Editar</button>
                <button class="btn btn-sm btn-danger" onclick="deleteUsuario(${u.id})">Desactivar</button>
            </td>
        </tr>
    `).join('');
}

function openModal() {
    editingId = null;
    document.getElementById('usuarioForm').reset();
    document.getElementById('modalTitle').textContent = 'Nuevo Usuario';
    document.getElementById('passwordField').style.display = 'block';
    document.getElementById('password').required = true;
    toggleModal('usuarioModal', true);
}

function closeModal() {
    toggleModal('usuarioModal', false);
    console.log("close Modal onclick");
}

async function editUsuario(id) {
    const usuario = usuariosData.find(u => u.id === id);
    if (!usuario) return;
    
    editingId = id;
    document.getElementById('nombre').value = usuario.nombre;
    document.getElementById('email').value = usuario.email;
    document.getElementById('rol').value = usuario.rol;
    document.getElementById('activo').value = usuario.activo ? 'true' : 'false';
    
    document.getElementById('modalTitle').textContent = 'Editar Usuario';
    document.getElementById('passwordField').style.display = 'none';
    document.getElementById('password').required = false;
    toggleModal('usuarioModal', true);
}

async function saveUsuario(e) {
    e.preventDefault();
    
    const data = {
        nombre: document.getElementById('nombre').value,
        email: document.getElementById('email').value,
        rol: document.getElementById('rol').value,
        activo: document.getElementById('activo').value === 'true'
    };
    
    const password = document.getElementById('password').value;
    if (password) {
        data.password = password;
    }
    
    try {
        toggleLoading(true);
        
        if (editingId) {
            await apiRequest(`/api/usuarios/${editingId}`, {
                method: 'PUT',
                body: JSON.stringify(data)
            });
            showAlert('Usuario actualizado correctamente', 'success');
        } else {
            if (!password) {
                showAlert('La contraseña es obligatoria para nuevos usuarios', 'error');
                return;
            }
            await apiRequest('/api/usuarios', {
                method: 'POST',
                body: JSON.stringify({...data, password})
            });
            showAlert('Usuario creado correctamente', 'success');
        }
        
        closeModal();
        loadUsuarios();
        
    } catch (error) {
        showAlert(error.message, 'error');
    } finally {
        toggleLoading(false);
    }
}

async function deleteUsuario(id) {
    if (!confirm('¿Esta seguro de desactivar este usuario?')) return;
    
    try {
        toggleLoading(true);
        await apiRequest(`/api/usuarios/${id}`, { method: 'DELETE' });
        showAlert('Usuario desactivado correctamente', 'success');
        loadUsuarios();
    } catch (error) {
        showAlert(error.message, 'error');
    } finally {
        toggleLoading(false);
    }
}