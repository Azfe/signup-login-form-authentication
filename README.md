# Sistema de Autenticación con JWT

Un sistema completo de autenticación con registro y login usando HTML5, CSS3, JavaScript para el frontend y Python (FastAPI) con JWT para el backend.

## 🚀 Características

- **Frontend responsivo** con HTML5, CSS3 y JavaScript vanilla
- **Backend robusto** con FastAPI y SQLAlchemy
- **Autenticación JWT** segura
- **Validación de formularios** tanto en frontend como backend
- **Base de datos SQLite** (fácil de cambiar a PostgreSQL/MySQL)
- **Interfaz moderna** con animaciones y efectos visuales
- **Manejo de errores** completo
- **CORS configurado** para desarrollo

## 📁 Estructura del Proyecto

```
auth-system/
├── frontend/
│   └── index.html          # Aplicación frontend completa
├── backend/
│   ├── main.py            # Aplicación FastAPI
│   ├── requirements.txt   # Dependencias Python
│   └── .env              # Variables de entorno
└── README.md             # Este archivo
```

## 🛠️ Instalación y Configuración

### Backend (Python)

1. **Crear directorio y entorno virtual:**
```bash
mkdir auth-system && cd auth-system
mkdir backend && cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. **Instalar dependencias:**
```bash
pip install fastapi==0.104.1
pip install uvicorn==0.24.0
pip install sqlalchemy==2.0.23
pip install python-jose[cryptography]==3.3.0
pip install passlib[bcrypt]==1.7.4
pip install python-multipart==0.0.6
pip install python-dotenv==1.0.0
```

3. **Crear archivo .env:**
```env
SECRET_KEY=tu-clave-secreta-muy-segura-aqui-cambiala-por-una-aleatoria
DATABASE_URL=sqlite:///./auth.db
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

4. **Ejecutar el servidor:**
```bash
python main.py
# O alternativamente:
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

1. **Crear directorio frontend:**
```bash
cd .. && mkdir frontend
# Copiar el contenido HTML en frontend/index.html
```

2. **Servir el frontend (opcional):**
```bash
# Con Python
cd frontend
python -m http.server 3000

# Con Node.js (si tienes instalado)
npx serve -s . -p 3000

# O simplemente abrir index.html en el navegador
```

## 🔧 Configuración de Variables de Entorno

Crea un archivo `.env` en el directorio backend:

```env
# Clave secreta para JWT (genera una aleatoria en producción)
SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7

# URL de la base de datos
DATABASE_URL=sqlite:///./auth.db

# Tiempo de expiración del token (en minutos)
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Para producción con PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost/dbname
```

## 🌐 Endpoints de la API

### Autenticación

- `POST /auth/register` - Registrar nuevo usuario
- `POST /auth/login` - Iniciar sesión
- `GET /auth/me` - Obtener información del usuario actual

### Gestión de Usuarios

- `GET /auth/users` - Obtener lista de usuarios (requiere autenticación)
- `DELETE /auth/users/{user_id}` - Eliminar usuario (solo el propio)

### Documentación

- `GET /` - Endpoint de prueba
- `GET /docs` - Documentación automática de Swagger
- `GET /redoc` - Documentación alternativa de ReDoc

## 📝 Uso de la API

### Registro de Usuario

```javascript
const response = await fetch('http://localhost:8000/auth/register', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    name: "Juan Pérez",
    email: "juan@ejemplo.com",
    password: "mipassword123"
  })
});
```

### Inicio de Sesión

```javascript
const response = await fetch('http://localhost:8000/auth/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: "juan@ejemplo.com",
    password: "mipassword123"
  })
});

const data = await response.json();
// data.access_token contiene el JWT
```

### Acceso a Rutas Protegidas

```javascript
const response = await fetch('http://localhost:8000/auth/me', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});
```

## 🔒 Seguridad

### Características de Seguridad Implementadas:

- **Hashing de contraseñas** con bcrypt
- **Tokens JWT** con expiración configurable
- **Validación de entrada** tanto en frontend como backend
- **CORS** configurado correctamente
- **Verificación de tokens** en rutas protegidas
- **Sanitización de datos** con Pydantic

### Recomendaciones para Producción:

1. **Cambiar la SECRET_KEY** por una clave aleatoria y segura
2. **Usar HTTPS** en producción
3. **Configurar variables de entorno** adecuadamente
4. **Usar una base de datos robusta** (PostgreSQL, MySQL)
5. **Implementar rate limiting**
6. **Agregar logging** para auditoría
7. **Validar y sanitizar** todas las entradas

## 🛡️ Validaciones Implementadas

### Frontend:
- Validación de email
- Confirmación de contraseña
- Longitud mínima de contraseña
- Campos requeridos
- Mensajes de error amigables

### Backend:
- Validación de esquemas con Pydantic
- Verificación de email único
- Validación de contraseña (mínimo 6 caracteres)
- Autenticación de credenciales
- Verificación de tokens JWT

## 🎨 Características del Frontend

### Diseño:
- **Interfaz moderna** con gradientes y efectos glass
- **Animaciones suaves** con CSS3
- **Responsive design** para móviles y desktop
- **Estados de carga** con spinners
- **Alertas contextuales** para feedback

### Funcionalidades:
- **Navegación fluida** entre formularios
- **Persistencia de sesión** con localStorage
- **Verificación automática** de tokens
- **Logout seguro** con limpieza de datos
- **Manejo de errores** completo

## 📊 Base de Datos

### Esquema de Usuario:

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Migración a PostgreSQL:

Para usar PostgreSQL en producción, cambiar en `.env`:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/auth_db
```

Y instalar el driver:
```bash
pip install psycopg2-binary
```

## 🧪 Testing

### Probar el Backend:

```bash
# Instalar dependencias de testing
pip install pytest pytest-asyncio httpx

# Crear tests (ejemplo)
# test_main.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_register():
    response = client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "testpass123"
        }
    )
    assert response.status_code == 200

def test_login():
    # Primero registrar
    client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "login@example.com", 
            "password": "testpass123"
        }
    )
    
    # Luego hacer login
    response = client.post(
        "/auth/login",
        json={
            "email": "login@example.com",
            "password": "testpass123"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
```

## 🚀 Despliegue

### Usando Docker:

```dockerfile
# Dockerfile
FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - SECRET_KEY=your-secret-key
      - DATABASE_URL=sqlite:///./auth.db
    volumes:
      - ./auth.db:/app/auth.db
```

### Variables de Entorno para Producción:

```env
SECRET_KEY=super-secret-key-for-production
DATABASE_URL=postgresql://user:pass@db:5432/authdb
ACCESS_TOKEN_EXPIRE_MINUTES=60
DEBUG=False
CORS_ORIGINS=["https://yourdomain.com"]
```

## 🔧 Personalización

### Agregar Nuevos Campos al Usuario:

1. **Modificar el modelo SQLAlchemy:**
```python
class User(Base):
    # ... campos existentes ...
    phone = Column(String, nullable=True)
    role = Column(String, default="user")
```

2. **Actualizar los esquemas Pydantic:**
```python
class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    role: str = "user"
```

### Agregar Roles y Permisos:

```python
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"

def require_role(required_role: UserRole):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role != required_role:
            raise HTTPException(
                status_code=403,
                detail="Insufficient permissions"
            )
        return current_user
    return role_checker

# Uso:
@app.get("/admin/users")
async def admin_only_route(user: User = Depends(require_role(UserRole.ADMIN))):
    # Solo admin puede acceder
    pass
```

## 📚 Recursos Adicionales

- [Documentación de FastAPI](https://fastapi.tiangolo.com/)
- [JWT.io](https://jwt.io/) - Para debuggear tokens JWT
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Pydantic Docs](https://docs.pydantic.dev/)

## 🐛 Troubleshooting

### Problemas Comunes:

1. **Error de CORS:**
   - Verificar que el frontend esté en los origins permitidos
   - Comprobar que las URLs coincidan exactamente

2. **Token inválido:**
   - Verificar que la SECRET_KEY sea la misma
   - Comprobar que el token no haya expirado

3. **Error de base de datos:**
   - Verificar que el archivo de BD tenga permisos de escritura
   - Para PostgreSQL, verificar conexión y credenciales

4. **Error de instalación:**
   - Usar un entorno virtual limpio
   - Verificar la versión de Python (3.7+)

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Libre para uso personal y comercial.