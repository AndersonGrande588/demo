const API_URL = 'http://localhost:8000';

function setToken(token) {
    localStorage.setItem('token', token);
}

function getToken() {
    return localStorage.getItem('token');
}

function setUser(user) {
    localStorage.setItem('user', JSON.stringify(user));
}

function getUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = 'index.html';
}

function checkAuth() {
    const token = getToken();
    if (!token) {
        window.location.href = 'index.html';
        return false;
    }
    return true;
}

function hasRole(roles) {
    const user = getUser();
    if (!user) return false;
    return roles.includes(user.rol);
}

async function apiRequest(endpoint, options = {}) {
    const token = getToken();
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };
    
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    try {
        const response = await fetch(`${API_URL}${endpoint}`, {
            ...options,
            headers
        });
        
        if (response.status === 401) {
            logout();
            return null;
        }
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Error en la peticion');
        }
        
        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 2
    }).format(amount);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-CO', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function showAlert(message, type = 'info') {
    const alert = document.getElementById('alert');
    if (alert) {
        alert.className = `alert alert-${type} show`;
        alert.textContent = message;
        setTimeout(() => {
            alert.classList.remove('show');
        }, 4000);
    }
}

function toggleLoading(show) {
    const loading = document.getElementById('loading');
    if (loading) {
        loading.classList.toggle('show', show);
    }
}

function toggleModal(modalId, show) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.toggle('active', show);
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}