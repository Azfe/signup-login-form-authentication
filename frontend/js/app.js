class AuthApp {
    constructor() {
        this.apiUrl = 'http://localhost:8000'; // URL del backend
        this.token = localStorage.getItem('token');
        this.init();
    }

    init() {
        this.bindEvents();
        this.checkAuth();
    }

    bindEvents() {
        // Navegación entre formularios
        document.getElementById('showRegister').addEventListener('click', () => {
            this.showForm('register');
        });

        document.getElementById('showLogin').addEventListener('click', () => {
            this.showForm('login');
        });

        // Formularios
        document.getElementById('login-form').addEventListener('submit', (e) => {
            this.handleLogin(e);
        });

        document.getElementById('register-form').addEventListener('submit', (e) => {
            this.handleRegister(e);
        });

        // Logout
        document.getElementById('logoutBtn').addEventListener('click', () => {
            this.handleLogout();
        });
    }

    showForm(formType) {
        const forms = document.querySelectorAll('.form-container');
        const dashboard = document.getElementById('dashboard');

        forms.forEach(form => form.classList.remove('active'));
        dashboard.classList.remove('active');

        if (formType === 'login') {
            document.getElementById('loginForm').classList.add('active');
        } else if (formType === 'register') {
            document.getElementById('registerForm').classList.add('active');
        }

        this.clearAlerts();
    }

    showDashboard() {
        const forms = document.querySelectorAll('.form-container');
        forms.forEach(form => form.classList.remove('active'));
        document.getElementById('dashboard').classList.add('active');
    }

    async handleLogin(e) {
        e.preventDefault();
        const btn = document.getElementById('loginBtn');
        const btnText = btn.querySelector('.btn-text');

        try {
            this.setLoading(btn, btnText, true);

            const formData = new FormData(e.target);
            const data = {
                email: formData.get('email'),
                password: formData.get('password')
            };

            const response = await fetch(`${this.apiUrl}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok) {
                localStorage.setItem('token', result.access_token);
                localStorage.setItem('user', JSON.stringify(result.user));
                this.token = result.access_token;

                this.showAlert('loginAlert', 'Inicio de sesión exitoso', 'success');
                setTimeout(() => {
                    this.showDashboard();
                    this.loadUserData();
                }, 1000);
            } else {
                this.showAlert('loginAlert', result.detail || 'Error al iniciar sesión', 'error');
            }
        } catch (error) {
            this.showAlert('loginAlert', 'Error de conexión con el servidor', 'error');
        } finally {
            this.setLoading(btn, btnText, false);
        }
    }

    async handleRegister(e) {
        e.preventDefault();
        const btn = document.getElementById('registerBtn');
        const btnText = btn.querySelector('.btn-text');

        try {
            this.setLoading(btn, btnText, true);

            const formData = new FormData(e.target);
            const password = formData.get('password');
            const confirmPassword = formData.get('confirmPassword');

            if (password !== confirmPassword) {
                this.showAlert('registerAlert', 'Las contraseñas no coinciden', 'error');
                return;
            }

            const data = {
                name: formData.get('name'),
                email: formData.get('email'),
                password: password
            };

            const response = await fetch(`${this.apiUrl}/auth/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok) {
                this.showAlert('registerAlert', 'Registro exitoso. Puedes iniciar sesión ahora.', 'success');
                setTimeout(() => {
                    this.showForm('login');
                    document.getElementById('register-form').reset();
                }, 2000);
            } else {
                this.showAlert('registerAlert', result.detail || 'Error en el registro', 'error');
            }
        } catch (error) {
            this.showAlert('registerAlert', 'Error de conexión con el servidor', 'error');
        } finally {
            this.setLoading(btn, btnText, false);
        }
    }

    handleLogout() {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        this.token = null;
        this.showForm('login');
    }

    checkAuth() {
        if (this.token) {
            this.verifyToken();
        }
    }

    async verifyToken() {
        try {
            const response = await fetch(`${this.apiUrl}/auth/me`, {
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });

            if (response.ok) {
                this.showDashboard();
                this.loadUserData();
            } else {
                this.handleLogout();
            }
        } catch (error) {
            this.handleLogout();
        }
    }

    loadUserData() {
        const user = JSON.parse(localStorage.getItem('user'));
        if (user) {
            document.getElementById('userName').textContent = user.name;
            document.getElementById('userEmail').textContent = user.email;
        }
    }

    showAlert(alertId, message, type) {
        const alert = document.getElementById(alertId);
        alert.className = `alert ${type}`;
        alert.textContent = message;
        alert.classList.add('show');

        setTimeout(() => {
            alert.classList.remove('show');
        }, 5000);
    }

    clearAlerts() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            alert.classList.remove('show');
        });
    }

    setLoading(btn, btnText, isLoading) {
        if (isLoading) {
            btn.disabled = true;
            btnText.innerHTML = '<span class="loading"></span>';
        } else {
            btn.disabled = false;
            btnText.innerHTML = btn.id === 'loginBtn' ? 'Iniciar Sesión' : 'Registrarse';
        }
    }
}

// Inicializar la aplicación
document.addEventListener('DOMContentLoaded', () => {
    new AuthApp();
});