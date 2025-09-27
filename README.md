# Sistema de Autenticación con JWT

Un sistema completo de autenticación con registro y login usando HTML5, CSS3, JavaScript para el frontend y Python (FastAPI) con JWT para el backend.

![Demo](https://img.shields.io/badge/Demo-Live-green)
![Python](https://img.shields.io/badge/Python-3.13%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🚀 Características

- 🎨 **Frontend responsivo** con HTML5, CSS3 y JavaScript vanilla
- ⚙ **Backend robusto** con FastAPI y SQLAlchemy
- 🔒 **Autenticación JWT**  segura con expiración configurable
- ✅ **Validación de formularios** tanto en frontend como backend
- 💾 **Base de datos SQLite** (fácil de cambiar a PostgreSQL/MySQL)
- 📱 **Diseño responsivo** con animaciones y efectos visuales
- ⚠ **Manejo de errores** completo
- 🌐 **CORS configurado** para desarrollo
- 📝 **Documentación automática** con Swagger UI

## 🖼️ Vista Previa

### Login

<!-- ![Vista previa de la app: Login](preview/Screenshot_login.png) -->

<img src="preview/Screenshot_login.png" alt="Vista previa de la app: Login" height="400"/>

### Registro

<!-- ![Vista previa de la app: Sign Up](preview/Screenshot_registro.png) -->

<img src="preview/Screenshot_registro.png" alt="Vista previa de la app: Sign Up" height="400"/>

## 📁 Estructura del Proyecto

```bash
auth-system/
├── 📁 frontend/
│   └── index.html              # Aplicación frontend completa
├── 📁 backend/
│   ├── main.py                # API FastAPI
│   ├── .env                   # Variables de entorno
│   ├── requirements.txt       # Dependencias Python
│   └── auth.db               # Base de datos SQLite (auto-generada)
├── README.md                  # Documentación del proyecto
└── .gitignore                # Archivos ignorados por Git
```

## 🛠️ Instalación y Configuración

### Prerrequisitos

- Python 3.13 o superior ([Descargar aquí](https://www.python.org/downloads/))
- Git ([Descargar aquí](https://git-scm.com/downloads))

### 📥 Clonar el Repositorio

```bash
git clone https://github.com/Azfe/signup-login-form-authentication.git
cd auth-system
```

### ⚙️ Configuración del Backend (Python)

#### 1. **Crear y activar entorno virtual:**

```bash
cd backend
python -m venv .venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

#### 2. **Instalar dependencias:**

```bash
pip install fastapi==0.115.0
pip install uvicorn==0.32.0
pip install sqlalchemy==2.0.36
pip install "python-jose[cryptography]==3.3.0"
pip install "passlib[bcrypt]==1.7.4"
pip install python-dotenv==1.0.1
pip install "pydantic[email]==2.9.0"
pip install email-validator==2.2.0
```

O usando requirements.txt:

```bash
pip install -r requirements.txt
```

#### 3. **Configurar variables de entorno:**

Crear archivo `.env` en la carpeta `backend/`:

```env
# Clave secreta para JWT (cambiar en producción)
SECRET_KEY=tu-clave-secreta-muy-segura-aqui-cambiala-por-una-aleatoria

# URL de la base de datos
DATABASE_URL=sqlite:///./auth.db

# Tiempo de expiración del token (en minutos)
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

#### 4. **Ejecutar el servidor backend:**

```bash
python main.py
# O alternativamente:
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

El backend estará disponible en: `http://localhost:8000`

### 🌐 Configuración del Frontend

#### 1. **Abrir nueva terminal y navegar al frontend:**

```bash
cd frontend
```

#### 2. **Servir el frontend:**

Opción A - Con Python:

```bash
python -m http.server 3000
```

Opción B - Con Node.js:

```bash
bashnpx serve -s . -p 3000
```

Opción C - Abrir directamente:

```bash
# Hacer doble clic en index.html
```

El frontend estará disponible en: `http://localhost:3000`

## 🎯 Uso de la Aplicación

### 1. Registrar Usuario

Abrir `http://localhost:3000`
Hacer clic en "Regístrate aquí"
Completar el formulario:

Nombre completo
Email válido
Contraseña (mínimo 6 caracteres)
Confirmar contraseña

Hacer clic en "Registrarse"

### 2. Iniciar Sesión

Ingresar email y contraseña
Hacer clic en "Iniciar Sesión"
Serás redirigido al dashboard

### 3. Dashboard

Ver información del usuario
Cerrar sesión cuando desees

## 🔧 Desarrollo

### Ejecutar en Modo Desarrollo

#### Terminal 1 - Backend

```bash
cd backend
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Terminal 2 - Frontend

```bash
cd frontend
python -m http.server 3000
```

## 🧪 Testing

### Ejecutar tests del backend

```bash
cd backend
pytest test_main.py -v
```

### Generar usuarios de prueba

```bash
python test_main.py --generate-users
```

## 🌐 Endpoints de la API

### Autenticación

- `POST /auth/register` - Registrar nuevo usuario
- `POST /auth/login` - Iniciar sesión
- `GET /auth/me` - Obtener información del usuario actual

### Usuarios

- `GET /auth/users` - Obtener lista de usuarios (requiere autenticación)
- `DELETE /auth/users/{user_id}` - Eliminar usuario (solo el propio)

### Documentación

- `GET /` - Endpoint de prueba
- `GET /docs` - Documentación automática de Swagger
- `GET /redoc` - Documentación alternativa de ReDoc

## 🔒 Seguridad

### Características de Seguridad Implementadas

- **Hashing de contraseñas** con bcrypt
- **Tokens JWT** con expiración configurable
- **Validación de entrada** tanto en frontend como backend
- **CORS** configurado correctamente
- **Verificación de tokens** en rutas protegidas
- **Sanitización de datos** con Pydantic

### Recomendaciones para Producción

1. **Cambiar la SECRET_KEY** por una clave aleatoria y segura
2. **Usar HTTPS** en producción
3. **Configurar variables de entorno** adecuadamente
4. **Usar una base de datos robusta** (PostgreSQL, MySQL)
5. **Implementar rate limiting**
6. **Agregar logging** para auditoría
7. **Variables de entorno seguras**

## 🚀 Despliegue

### Docker (recomendado)

Crear `Dockerfile` en backend:

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Ejecutar:

```bash
cd backend
docker build -t auth-system .
docker run -p 8000:8000 auth-system
```

Variables de Entorno para Producción

```env
SECRET_KEY=super-secret-production-key-here
DATABASE_URL=postgresql://user:pass@localhost/authdb
ACCESS_TOKEN_EXPIRE_MINUTES=60
DEBUG=False
CORS_ORIGINS=["https://yourdomain.com"]
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crear rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📝 Changelog

### v1.0.0 (2024-XX-XX)

- ✨ Sistema completo de autenticación
- 🎨 Frontend responsivo con CSS3
- 🔐 Backend con FastAPI y JWT
- 📱 Dashboard de usuario
- ✅ Validaciones completas
- 🧪 Tests unitarios

## 🐛 Problemas Conocidos

- Python 3.13: Usar Python 3.11 o 3.12 para mejor compatibilidad
- CORS: Verificar que el frontend esté en los origins permitidos

## 📚 Recursos

- <[FastAPI Documentation](https://fastapi.tiangolo.com/)>
- <[JWT.io](https://jwt.io/)> - Debug JWT tokens
- <[SQLAlchemy Docs](https://docs.sqlalchemy.org/)>
- <[Pydantic Docs](https://docs.pydantic.dev/)>

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.

## 👨‍💻 Autor

### Alex Zapata

- GitHub: <[@azfe](https://github.com/azfe)>
- Email: <[alexzapata1984@gmail.com](mailto:alexzapata1984@gmail.com)>

### 🌟 Agradecimientos

- <[FastAPI](https://fastapi.tiangolo.com/)> por el excelente framework
- [SQLAlchemy](https://sqlalchemy.org/) por el ORM
- [Pydantic](https://pydantic-docs.helpmanual.io/) por la validación de datos

#### ⭐ Si este proyecto te ayudó, dale una estrella en GitHub! ⭐

## 🚀 Demo en Vivo

[Ver Demo](https://azup.form-auth.com) | [Documentación API](https://https://azup.form-auth.com/docs)

## 📞 Soporte

Si tienes problemas:

1. Revisa la sección de Issues
2. Crea un nuevo issue con detalles del problema
3. Incluye tu versión de Python y sistema operativo
