# Sistema de Gestión de Clientes

Sistema integrado de gestión de clientes con aplicación de escritorio (Tkinter), API REST (Flask) y base de datos MySQL.

## Arquitectura

```
ESCRITORIO (Tkinter) ──HTTP──> API REST (Flask) ──SQL──> MySQL (phpMyAdmin)
```

## Requisitos Previos

- Python 3.10+
- MySQL (XAMPP / phpMyAdmin)
- pip

## Instalación

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd idl-2
```

### 2. Instalar dependencias Python

```bash
pip install -r requirements.txt
```

### 3. Configurar la base de datos

1. Inicia XAMPP y asegúrate de que MySQL esté activo.
2. Abre phpMyAdmin (`http://localhost/phpmyadmin`).
3. Importa el archivo `database/schema.sql` (crea la BD `gestion_clientes` con tablas y un usuario admin).

### 4. Configurar variables de entorno (opcional)

Crea un archivo `.env` en la raíz del proyecto para personalizar la configuración:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=gestion_clientes
JWT_SECRET_KEY=cambia-este-secreto-en-produccion
FLASK_DEBUG=False
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
```

### 5. Iniciar el servidor API

```bash
python -m api.app
```

El servidor queda disponible en `http://localhost:5000`.

### 6. Iniciar la aplicación de escritorio

En otra terminal:

```bash
python desktop/main.py
```

## Credenciales por defecto

| Campo      | Valor               |
|------------|---------------------|
| Email      | admin@sistema.com   |
| Contraseña | admin123            |
| Rol        | admin               |

## Endpoints API

| Método | URL                        | Descripción                         |
|--------|----------------------------|-------------------------------------|
| POST   | /api/auth/login            | Autenticar usuario → retorna JWT    |
| POST   | /api/auth/register         | Registrar usuario (solo admin)      |
| GET    | /api/auth/perfil           | Datos del usuario autenticado       |
| GET    | /api/clientes              | Listar clientes (paginado)          |
| GET    | /api/clientes/buscar?q=... | Buscar clientes                     |
| GET    | /api/clientes/{id}         | Obtener cliente por ID              |
| POST   | /api/clientes              | Crear cliente                       |
| PUT    | /api/clientes/{id}         | Actualizar cliente                  |
| DELETE | /api/clientes/{id}         | Eliminar cliente (soft-delete)      |
| GET    | /api/health                | Verificar estado del servidor       |

Todos los endpoints de `/api/clientes` requieren header `Authorization: Bearer <token>`.

## Estructura del Proyecto

```
├── README.md
├── requirements.txt
├── .gitignore
├── database/
│   └── schema.sql
├── api/
│   ├── app.py
│   ├── config.py
│   ├── models/
│   │   ├── usuario.py
│   │   └── cliente.py
│   ├── routes/
│   │   ├── auth_routes.py
│   │   └── cliente_routes.py
│   ├── middleware/
│   │   └── auth_middleware.py
│   └── utils/
│       └── database.py
└── desktop/
    ├── main.py
    ├── api_client.py
    ├── views/
    │   ├── login_view.py
    │   ├── dashboard_view.py
    │   ├── cliente_form.py
    │   └── cliente_list.py
    └── utils/
        └── session.py
```

## Tecnologías

- **Backend**: Python, Flask, Flask-JWT-Extended, PyMySQL, bcrypt
- **Frontend de escritorio**: Tkinter (incluido en Python)
- **Base de datos**: MySQL (XAMPP / phpMyAdmin)
- **Autenticación**: JWT + bcrypt
- **Comunicación**: HTTP/REST con `requests`
