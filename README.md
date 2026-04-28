# Service Persistence NotebookUm

Este microservicio es el **Gestor de la Base de Datos** para el sistema NotebookUm.

## Responsabilidades
- Es el único servicio con acceso directo a MySQL.
- Maneja las migraciones mediante Alembic.
- Recibe peticiones HTTP del Controlador para realizar operaciones CRUD (Create, Read, Update, Delete) sobre historiales, documentos y usuarios.

## Ejecución con Docker
```bash
docker-compose up -d --build
```
El servicio estará disponible internamente en el puerto `5003`.
Asegúrate de configurar las variables de entorno de base de datos (`DB_HOST`, `DB_PASSWORD`, etc.).
