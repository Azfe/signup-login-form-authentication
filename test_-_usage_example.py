# test_main.py - Archivo de tests para el backend
import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, get_db, Base, User
import json

# Base de datos en memoria para tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear tablas de test
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Fixtures
@pytest.fixture
def test_user_data():
    return {
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpass123"
    }

@pytest.fixture
def test_login_data():
    return {
        "email": "test@example.com",
        "password": "testpass123"
    }

# Tests de la API
class TestAuth:
    
    def test_root_endpoint(self):
        """Test del endpoint raíz"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "API de Autenticación funcionando correctamente"}

    def test_register_success(self, test_user_data):
        """Test de registro exitoso"""
        response = client.post("/auth/register", json=test_user_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == test_user_data["name"]
        assert data["email"] == test_user_data["email"]
        assert "id" in data
        assert "created_at" in data

    def test_register_duplicate_email(self, test_user_data):
        """Test de registro con email duplicado"""
        # Primer registro
        client.post("/auth/register", json=test_user_data)
        
        # Segundo registro con mismo email
        response = client.post("/auth/register", json=test_user_data)
        assert response.status_code == 400
        assert "El email ya está registrado" in response.json()["detail"]

    def test_register_short_password(self):
        """Test de registro con contraseña corta"""
        user_data = {
            "name": "Test User",
            "email": "short@example.com",
            "password": "123"
        }
        response = client.post("/auth/register", json=user_data)
        assert response.status_code == 400
        assert "al menos 6 caracteres" in response.json()["detail"]

    def test_register_invalid_email(self):
        """Test de registro con email inválido"""
        user_data = {
            "name": "Test User",
            "email": "invalid-email",
            "password": "testpass123"
        }
        response = client.post("/auth/register", json=user_data)
        assert response.status_code == 422

    def test_login_success(self, test_user_data, test_login_data):
        """Test de login exitoso"""
        # Registrar usuario primero
        client.post("/auth/register", json=test_user_data)
        
        # Intentar login
        response = client.post("/auth/login", json=test_login_data)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data

    def test_login_wrong_password(self, test_user_data):
        """Test de login con contraseña incorrecta"""
        # Registrar usuario
        client.post("/auth/register", json=test_user_data)
        
        # Login con contraseña incorrecta
        wrong_data = {
            "email": test_user_data["email"],
            "password": "wrongpassword"
        }
        response = client.post("/auth/login", json=wrong_data)
        assert response.status_code == 401
        assert "Email o contraseña incorrectos" in response.json()["detail"]

    def test_login_nonexistent_user(self):
        """Test de login con usuario inexistente"""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "anypassword"
        }
        response = client.post("/auth/login", json=login_data)
        assert response.status_code == 401

    def test_get_current_user_success(self, test_user_data, test_login_data):
        """Test de obtener usuario actual con token válido"""
        # Registrar y hacer login
        client.post("/auth/register", json=test_user_data)
        login_response = client.post("/auth/login", json=test_login_data)
        token = login_response.json()["access_token"]
        
        # Obtener información del usuario
        response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user_data["email"]
        assert data["name"] == test_user_data["name"]

    def test_get_current_user_no_token(self):
        """Test de obtener usuario sin token"""
        response = client.get("/auth/me")
        assert response.status_code == 403

    def test_get_current_user_invalid_token(self):
        """Test de obtener usuario con token inválido"""
        response = client.get("/auth/me", headers={"Authorization": "Bearer invalid_token"})
        assert response.status_code == 401

    def test_get_users_authenticated(self, test_user_data, test_login_data):
        """Test de obtener lista de usuarios (autenticado)"""
        # Registrar y hacer login
        client.post("/auth/register", json=test_user_data)
        login_response = client.post("/auth/login", json=test_login_data)
        token = login_response.json()["access_token"]
        
        # Obtener lista de usuarios
        response = client.get("/auth/users", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_get_users_unauthenticated(self):
        """Test de obtener usuarios sin autenticación"""
        response = client.get("/auth/users")
        assert response.status_code == 403

# Ejemplos de uso del cliente JavaScript
class ClientExamples:
    """
    Ejemplos de cómo usar la API desde JavaScript
    """
    
    @staticmethod
    def example_register():
        return """
        // Ejemplo de registro
        async function registerUser(userData) {
            try {
                const response = await fetch('http://localhost:8000/auth/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        name: userData.name,
                        email: userData.email,
                        password: userData.password
                    })
                });
                
                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.detail);
                }
                
                const result = await response.json();
                console.log('Usuario registrado:', result);
                return result;
            } catch (error) {
                console.error('Error en registro:', error.message);
                throw error;
            }
        }
        
        // Uso
        registerUser({
            name: 'Juan Pérez',
            email: 'juan@ejemplo.com',
            password: 'mipassword123'
        });
        """
    
    @staticmethod
    def example_login():
        return """
        // Ejemplo de login
        async function loginUser(credentials) {
            try {
                const response = await fetch('http://localhost:8000/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        email: credentials.email,
                        password: credentials.password
                    })
                });
                
                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.detail);
                }
                
                const result = await response.json();
                
                // Guardar token en localStorage
                localStorage.setItem('token', result.access_token);
                localStorage.setItem('user', JSON.stringify(result.user));
                
                console.log('Login exitoso:', result);
                return result;
            } catch (error) {
                console.error('Error en login:', error.message);
                throw error;
            }
        }
        
        // Uso
        loginUser({
            email: 'juan@ejemplo.com',
            password: 'mipassword123'
        });
        """
    
    @staticmethod
    def example_authenticated_request():
        return """
        // Ejemplo de petición autenticada
        async function makeAuthenticatedRequest(url, options = {}) {
            const token = localStorage.getItem('token');
            
            if (!token) {
                throw new Error('No hay token de autenticación');
            }
            
            const headers = {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
                ...options.headers
            };
            
            try {
                const response = await fetch(url, {
                    ...options,
                    headers
                });
                
                if (response.status === 401) {
                    // Token expirado, redirigir a login
                    localStorage.removeItem('token');
                    localStorage.removeItem('user');
                    window.location.href = '/login';
                    return;
                }
                
                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.detail);
                }
                
                return await response.json();
            } catch (error) {
                console.error('Error en petición autenticada:', error.message);
                throw error;
            }
        }
        
        // Ejemplos de uso
        
        // Obtener perfil del usuario
        async function getUserProfile() {
            return await makeAuthenticatedRequest('http://localhost:8000/auth/me');
        }
        
        // Obtener lista de usuarios
        async function getUsers() {
            return await makeAuthenticatedRequest('http://localhost:8000/auth/users');
        }
        
        // Eliminar cuenta propia
        async function deleteAccount(userId) {
            return await makeAuthenticatedRequest(
                `http://localhost:8000/auth/users/${userId}`, 
                { method: 'DELETE' }
            );
        }
        """

# Utilidades para desarrollo
class DevUtils:
    """
    Utilidades para desarrollo y debugging
    """
    
    @staticmethod
    def generate_test_users():
        """Generar usuarios de prueba"""
        test_users = [
            {
                "name": "Admin User",
                "email": "admin@test.com",
                "password": "admin123"
            },
            {
                "name": "Regular User",
                "email": "user@test.com", 
                "password": "user123"
            },
            {
                "name": "Test User",
                "email": "test@test.com",
                "password": "test123"
            }
        ]
        
        for user in test_users:
            try:
                response = client.post("/auth/register", json=user)
                if response.status_code == 200:
                    print(f"Usuario creado: {user['email']}")
                else:
                    print(f"Error creando {user['email']}: {response.json()}")
            except Exception as e:
                print(f"Error: {e}")

    @staticmethod
    def decode_jwt_token(token):
        """Decodificar token JWT para debugging"""
        import jwt
        from main import SECRET_KEY, ALGORITHM
        
        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return decoded
        except jwt.ExpiredSignatureError:
            return {"error": "Token expirado"}
        except jwt.InvalidTokenError:
            return {"error": "Token inválido"}

# Script para ejecutar tests
if __name__ == "__main__":
    # Para ejecutar los tests:
    # pytest test_main.py -v
    
    # Para generar usuarios de prueba:
    # python test_main.py --generate-users
    
    import sys
    
    if "--generate-users" in sys.argv:
        print("Generando usuarios de prueba...")
        DevUtils.generate_test_users()
    else:
        print("Ejecuta: pytest test_main.py -v")
        print("Para generar usuarios: python test_main.py --generate-users")