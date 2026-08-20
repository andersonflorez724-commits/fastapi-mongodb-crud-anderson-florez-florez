# TechGear - Sistema Híbrido de Catálogo y Pedidos

Sistema web híbrido para una tienda de hardware y accesorios tecnológicos.

- **`techgear_api/`** — microservicio REST construido con **FastAPI** que administra el inventario y los pedidos sobre **MongoDB Atlas**, documentado con **Swagger UI**.
- **`techgear_web/`** — portal web construido con **Django** (patrón MVT) que consume la API mediante peticiones HTTP con la librería `requests` para mostrar el catálogo y permitir la creación de pedidos.

---

## Arquitectura

```
Navegador ──HTML──> Django (MVT, :8001) ──HTTP/JSON──> FastAPI (:8000) ──> MongoDB Atlas
```

Django nunca habla con MongoDB y FastAPI nunca renderiza HTML. El único contrato entre ambos servicios es JSON.

---

## Requisitos previos

- **Python 3.11** o superior
- Una cuenta de **MongoDB Atlas** con un clúster creado

---

## Puesta en marcha

### 1. Obtener la cadena de conexión de MongoDB Atlas

En Atlas: **Database → Connect → Drivers**. Se recomienda crear un usuario dedicado con rol `readWrite` sobre la base de datos y restringir el acceso de red a la IP propia.

### 2. Levantar la API FastAPI (terminal 1)

```bash
cd techgear_api

python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux / macOS

pip install -r requirements.txt

copy .env.example .env         # Windows (cp en Linux/macOS)
# Editar .env y completar MONGODB_URL con la cadena de Atlas

uvicorn main:app --reload --port 8000
```

| Recurso | URL |
|---|---|
| Documentación interactiva (Swagger UI) | http://localhost:8000/docs |
| Documentación alternativa (ReDoc) | http://localhost:8000/redoc |
| Estado del servicio | http://localhost:8000/ |

### 3. Levantar el portal Django (terminal 2)

```bash
cd techgear_web

python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux / macOS

pip install -r requirements.txt

copy .env.example .env         # Windows (cp en Linux/macOS)
# Editar .env y completar TECHGEAR_API_BASE_URL

python manage.py runserver 8001
```

| Recurso | URL |
|---|---|
| Catálogo de productos | http://localhost:8001/ |
| Crear pedido | http://localhost:8001/crear-pedido/ |

---

## Variables de entorno

Ningún archivo `.env` se versiona. Cada servicio incluye su `.env.example` con la lista completa de variables.

### `techgear_api/.env`

| Variable | Descripción | Ejemplo |
|---|---|---|
| `MONGODB_URL` | Cadena de conexión de Atlas | `mongodb+srv://<usuario>:<password>@<cluster>.mongodb.net/` |

### `techgear_web/.env`

| Variable | Descripción | Ejemplo |
|---|---|---|
| `DJANGO_SECRET_KEY` | Clave criptográfica de Django | `clave-solo-para-desarrollo` |
| `DJANGO_DEBUG` | Modo depuración | `True` |
| `DJANGO_ALLOWED_HOSTS` | Hosts autorizados | `localhost,127.0.0.1` |
| `TECHGEAR_API_BASE_URL` | URL base de la API | `http://localhost:8000` |
| `TECHGEAR_API_TIMEOUT` | Segundos de espera por petición | `10` |

---

## Endpoints de la API

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/` | Estado del servicio |
| `GET` | `/productos` | Listado de productos |
| `POST` | `/productos` | Crear producto |
| `GET` | `/productos/{id}` | Consultar producto |
| `PUT` | `/productos/{id}` | Actualizar producto |
| `DELETE` | `/productos/{id}` | Eliminar producto |
| `GET` | `/pedidos` | Listado de pedidos |
| `POST` | `/pedidos` | Registrar pedido |

---

## Autor

Taller 2 — TechGear: Sistema Híbrido de Catálogo y Pedidos (FastAPI + Django MVT).