document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
});

async function handleLogin(e) {
    e.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);
    
    try {
        toggleLoading(true);
        
        const response = await fetch(`${API_URL}/api/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Error al iniciar sesion');
        }
        
        setToken(data.access_token);
        setUser(data.usuario);
        
        window.location.href = 'dashboard.html';
        
    } catch (error) {
        showAlert(error.message, 'error');
    } finally {
        toggleLoading(false);
    }
}