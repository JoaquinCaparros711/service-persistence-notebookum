# 🗄️ Service Persistence NotebookUm (Python)

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0+-darkgreen.svg?style=flat-square&logo=flask&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red.svg?style=flat-square&logo=sqlalchemy&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-blue.svg?style=flat-square&logo=mysql&logoColor=white)

Este microservicio en Python/Flask implementa la **capa de acceso y manipulación de datos relacionales** para el sistema NotebookUm. Proporciona una interfaz RESTful de persistencia interna directa a la base de datos MySQL/MariaDB.

---

## 📋 Responsabilidades

- **Abstracción del Acceso a Datos:** Exponer operaciones CRUD para todas las entidades del negocio (usuarios, libretas, documentos históricos, conversaciones, mensajes y resúmenes).
- **Mapeo Objeto-Relacional (ORM):** Representación orientada a objetos de la base de datos utilizando SQLAlchemy.
- **Evolución del Esquema:** Control de versiones del esquema de base de datos a través de migraciones automatizadas con Alembic.
- **Rendimiento de Consultas:** Soporte nativo para separar lecturas y escrituras mediante binds de réplica de base de datos (Lectura/Escritura segregada).

---

## ⚡ Características Clave

- **Estilo RESTful Estandarizado:** Rutas uniformes para manipulación de recursos con respuestas y códigos de estado semánticos.
- **Manejo de Errores RFC 9457:** Los fallos de validación, errores de base de datos o excepciones HTTP devuelven un esquema estandarizado de `Problem Details`.
- **Cabeceras de Seguridad:** Uso de Flask-Talisman para forzar HSTS y añadir políticas de seguridad HTTP en entornos de producción.
- **Segregación de Conexiones (Read/Write Replica):** Redirige las operaciones de escritura al nodo primario de MySQL (`DB_WRITE_HOST`) y las consultas de lectura a la réplica (`DB_READ_HOST`).

---

## 🌐 Endpoints de la API (Interna)

Todas las rutas operan bajo el prefijo `/api/v1` y manejan la representación JSON del esquema:

| Método | Ruta | Entidad | Descripción |
| :--- | :--- | :--- | :--- |
| **GET** | `/health` | Sistema | Comprueba la salud del microservicio y la conexión activa con MySQL. |
| **GET** | `/api/v1/users` | Usuario | Lista todos los usuarios registrados. |
| **POST** | `/api/v1/users` | Usuario | Crea un nuevo registro de usuario. |
| **GET** | `/api/v1/users/<id>` | Usuario | Obtiene un usuario específico por su identificador único. |
| **PATCH** | `/api/v1/users/<id>` | Usuario | Actualiza de forma parcial los datos de un usuario. |
| **DELETE** | `/api/v1/users/<id>` | Usuario | Elimina lógicamente o físicamente un usuario por su ID. |
| **GET** | `/api/v1/documents` | Documento | Lista documentos de la base de datos (filtra por `user_id` opcionalmente). |
| **POST** | `/api/v1/documents` | Documento | Almacena los metadatos de un nuevo documento PDF. |
| **GET** | `/api/v1/documents/<id>` | Documento | Obtiene los detalles de un documento. |
| **PATCH** | `/api/v1/documents/<id>` | Documento | Actualiza campos del documento (ej. texto extraído o estado). |
| **DELETE** | `/api/v1/documents/<id>` | Documento | Elimina metadatos de un documento. |
| **GET** | `/api/v1/notebooks` | Libreta | Lista libretas del usuario (`user_id`). |
| **POST** | `/api/v1/notebooks` | Libreta | Crea una libreta (notebook) nueva. |
| **GET / PATCH / DELETE**| `/api/v1/notebooks/<id>`| Libreta | Operaciones individuales sobre una libreta. |
| **GET / POST** | `/api/v1/conversations`| Conversación| Operaciones de listado y creación de conversaciones. |
| **GET / PATCH / DELETE**| `/api/v1/conversations/<id>`| Conversación| Operaciones individuales sobre una conversación. |
| **GET / POST** | `/api/v1/messages` | Mensaje | Operaciones de listado y creación de mensajes de chat. |
| **GET / POST** | `/api/v1/summaries` | Resumen | Operaciones de listado y creación de resúmenes de documentos. |
| **GET / PATCH / DELETE**| `/api/v1/summaries/<id>`| Resumen | Operaciones individuales sobre un resumen de documento. |

---

## ⚙️ Configuración (Variables de Entorno)

A diferencia de otros componentes, este microservicio lee directamente la configuración desde las variables de entorno de su contenedor o sistema anfitrión:

| Variable de Entorno | Valor por Defecto | Descripción |
| :--- | :--- | :--- |
| `FLASK_ENV` | `development` | Entorno de ejecución (`production`, `development`, `testing`). |
| `PORT` | `5000` | Puerto en el que escucha el servidor Flask local. |
| `DB_USER` | `notebookum_user` | Usuario para autenticarse contra el motor MySQL. |
| `DB_PASSWORD` | `notebookum_password`| Contraseña de la base de datos. |
| `DB_NAME` | `notebookum_db` | Nombre de la base de datos relacional. |
| `DB_WRITE_HOST` | `mysql-primary` | Dirección del nodo primario de base de datos (para escrituras). |
| `DB_READ_HOST` | `mysql-replica` | Dirección del nodo réplica de base de datos (para lecturas). |
| `ALLOWED_ORIGINS` | `http://localhost:3000`| Orígenes CORS permitidos (separados por comas). |

---

## 🚀 Despliegue y Ejecución

### Ejecución Local

1. Instalar dependencias requeridas en tu entorno de desarrollo Python:
   ```bash
   pip install -r requirements.txt
   ```

2. Configurar variables de entorno y arrancar el servidor:
   ```bash
   export FLASK_ENV=development
   export DB_USER=root
   export DB_PASSWORD=password
   export DB_NAME=notebookum
   export DB_WRITE_HOST=127.0.0.1
   export DB_READ_HOST=127.0.0.1
   flask run --port=5003
   ```

3. Aplicar migraciones pendientes con Alembic:
   ```bash
   alembic upgrade head
   ```

### Despliegue en Docker

El despliegue con Docker Compose autogestiona réplicas balanceadas y asocia el microservicio a las redes aisladas para comunicarse con la base de datos y Traefik.

```bash
docker-compose up -d --build
```
