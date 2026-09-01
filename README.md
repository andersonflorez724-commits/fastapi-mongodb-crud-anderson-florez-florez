# 🖥️ TechGear — Sistema Híbrido de Catálogo y Pedidos

> Plataforma web híbrida para una tienda de hardware y accesorios tecnológicos. Arquitectura desacoplada: **Django** renderiza vistas, **FastAPI** gestiona datos y **MongoDB Atlas** almacena la información.

---

## 📦 Arquitectura del Sistema

```
┌──────────────┐       HTTP / JSON        ┌──────────────┐       Async Driver       ┌────────────────┐
│              │  ──────────────────────►  │              │  ──────────────────────►  │                │
│   Django     │                           │   FastAPI    │                           │  MongoDB Atlas │
│   (MVT)      │  ◄──────────────────────  │   (REST)     │  ◄──────────────────────  │                │
│   :8001      │       JSON Response       │   :8000      │       Queries             │                │
└──────────────┘                           └──────────────┘                           └────────────────┘
     Web UI                                  API Backend                               Base de Datos
```

Django **nunca** habla con MongoDB y FastAPI **nunca** renderiza HTML. El único contrato entre ambos servicios es **JSON**.

---

## 🛠️ Stack Tecnológico

| Capa | Tecnología | Propósito |
|------|-----------|-----------|
| **API REST** | FastAPI + Uvicorn | Backend asíncrono de alto rendimiento |
| **Base de datos** | MongoDB Atlas + Motor | NoSQL con driver async nativo para Python |
| **Portal Web** | Django (MVT) | Frontend server-rendered con templates |
| **Validación** | Pydantic | Schemas tipados y validación automática |
| **HTTP Client** | Requests | Consumo de la API desde Django |
| **Despliegue** | Render | Hosting de ambos servicios en la nube |

---

## ✨ Funcionalidades

- 🛒 **Catálogo de productos** — Listado, creación, edición y eliminación de productos
- 📦 **Gestión de inventario** — Control automático de stock al crear pedidos
- 🧾 **Sistema de pedidos** — Registro de pedidos con validación de stock en tiempo real
- 📄 **Documentación automática** — Swagger UI y ReDoc generados por FastAPI
- 🌐 **Portal web responsive** — Interfaz amigable construida con Django templates

---

## 🌍 Endpoints de Producción

| Servicio | URL |
|----------|-----|
| 🌐 Portal Web (Django) | [https://techgear-web.onrender.com](https://techgear-web.onrender.com/) |
| 📡 API REST (FastAPI) | [https://techgear-api.onrender.com](https://techgear-api.onrender.com/) |
| 📖 Swagger UI | [https://techgear-api.onrender.com/docs](https://techgear-api.onrender.com/docs) |
| 📖 ReDoc | [https://techgear-api.onrender.com/redoc](https://techgear-api.onrender.com/redoc) |

---

## 📁 Estructura del Proyecto

```
techgear/
├── techgear_api/                # Backend API (FastAPI)
│   ├── main.py                  # Endpoints y lógica de negocio
│   ├── database.py              # Conexión a MongoDB Atlas (Motor)
│   ├── schemas.py               # Modelos Pydantic (request/response)
│   ├── requirements.txt         # Dependencias de la API
│   ├── .env.example             # Plantilla de variables de entorno
│   └── .env                     # Variables reales (no se versiona)
│
├── techgear_web/                # Portal Web (Django)
│   ├── manage.py                # CLI de Django
│   ├── techgear_web/            # Configuración del proyecto Django
│   │   ├── settings.py          # Configuración principal
│   │   └── urls.py              # Enrutador principal
│   ├── catalogo/                # App principal
│   │   ├── views.py             # Vistas (controladores)
│   │   ├── urls.py              # Rutas de la app
│   │   ├── services.py          # Consumo de la API externa
│   │   ├── models.py            # Modelos Django (vacíos - DB en Mongo)
│   │   ├── admin.py             # Registro en Django Admin
│   │   └── templates/           # Templates HTML
│   │       └── catalogo/
│   │           ├── base.html
│   │           ├── catalogo.html
│   │           ├── crear_producto.html
│   │           ├── editar_producto.html
│   │           ├── crear_pedido.html
│   │           ├── ver_pedidos.html
│   │           └── detalle_pedido.html
│   ├── requirements.txt         # Dependencias de Django
│   └── vercel.json              # Configuración de despliegue
│
└── README.md                    # Este archivo
```

---

## 🚀 Puesta en Marcha

### Requisitos Previos

- **Python 3.11** o superior
- Una cuenta de **MongoDB Atlas** con un clúster creado

---

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/techgear.git
cd techgear
```

### 2. Obtener la cadena de conexión de MongoDB Atlas

1. Entra a [MongoDB Atlas](https://cloud.mongodb.com/)
2. Ve a **Database → Connect → Drivers**
3. Crea un usuario dedicado con rol `readWrite`
4. Restringe el acceso de red a tu IP

### 3. Levantar la API FastAPI (Terminal 1)

```bash
cd techgear_api

python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

pip install -r requirements.txt

cp .env.example .env            # Linux / macOS
copy .env.example .env          # Windows

# Editar .env y agregar tu MONGODB_URL
```

```bash
uvicorn main:app --reload --port 8000
```

| Recurso | URL |
|---------|-----|
| Swagger UI | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |
| Health Check | http://localhost:8000/ |

### 4. Levantar el Portal Django (Terminal 2)

```bash
cd techgear_web

python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

pip install -r requirements.txt

cp .env.example .env            # Linux / macOS
copy .env.example .env          # Windows

# Editar .env y agregar TECHGEAR_API_BASE_URL
```

```bash
python manage.py runserver 8001
```

| Recurso | URL |
|---------|-----|
| Catálogo de productos | http://localhost:8001/ |
| Crear pedido | http://localhost:8001/crear-pedido/ |
| Ver pedidos | http://localhost:8001/pedidos/ |

---

## 🔐 Variables de Entorno

Ningún archivo `.env` se versiona. Cada servicio incluye su `.env.example`.

### `techgear_api/.env`

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `MONGODB_URL` | Cadena de conexión de Atlas | `mongodb+srv://user:pass@cluster.mongodb.net/` |

### `techgear_web/.env`

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `DJANGO_SECRET_KEY` | Clave criptográfica | `clave-solo-para-desarrollo` |
| `DJANGO_DEBUG` | Modo depuración | `True` |
| `DJANGO_ALLOWED_HOSTS` | Hosts autorizados | `localhost,127.0.0.1` |
| `TECHGEAR_API_BASE_URL` | URL base de la API | `http://localhost:8000` |
| `TECHGEAR_API_TIMEOUT` | Timeout de peticiones (seg) | `10` |

---

## 📡 Endpoints de la API

### Productos

| Método | Ruta | Descripción | Código |
|--------|------|-------------|--------|
| `GET` | `/productos` | Listar todos los productos | 200 |
| `POST` | `/productos` | Crear un nuevo producto | 201 |
| `GET` | `/productos/{id}` | Obtener un producto por ID | 200 |
| `PUT` | `/productos/{id}` | Actualizar un producto | 200 |
| `DELETE` | `/productos/{id}` | Eliminar un producto | 200 |

### Pedidos

| Método | Ruta | Descripción | Código |
|--------|------|-------------|--------|
| `GET` | `/pedidos` | Listar todos los pedidos | 200 |
| `POST` | `/pedidos` | Crear un pedido (descuenta stock) | 201 |
| `GET` | `/pedidos/{id}` | Obtener un pedido por ID | 200 |

### Ejemplo de Producto (JSON)

```json
{
  "nombre": "Mouse Gamer RGB",
  "descripcion": "Mouse óptico con 16000 DPI y iluminación RGB personalizable",
  "precio": 49.99,
  "stock": 150,
  "categoria": "Periféricos",
  "imagen_url": "https://ejemplo.com/mouse.jpg"
}
```

### Ejemplo de Pedido (JSON)

```json
{
  "cliente": "Juan Pérez",
  "productos": [
    {
      "producto_id": "64f8a1b2c3d4e5f6a7b8c9d0",
      "cantidad": 2
    }
  ]
}
```

---

## 🤝 Contribuir

1. Haz un **fork** del repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Haz commit de tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un **Pull Request**

---

## 📄 Licencia

Este proyecto es parte de un taller académico. Distribución educativa.

---

## 👨‍💻 Autor

**Taller 2** — TechGear: Sistema Híbrido de Catálogo y Pedidos

*FastAPI + Django MVT + MongoDB Atlas*
