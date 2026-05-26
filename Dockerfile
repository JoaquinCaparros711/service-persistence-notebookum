FROM python:3.12-slim

# Security: Evitar compilacion de pyc files y buffer
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crear un usuario y grupo no-root
RUN groupadd -r notebookum_user && useradd -r -g notebookum_user notebookum_user

WORKDIR /app

# Instalar dependencias del sistema requeridas para build
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Obtener UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copiar archivos de requerimientos e instalar dependencias
COPY pyproject.toml uv.lock* ./
RUN uv sync

# Copiar el codigo del proyecto
COPY . .

# Restringir permisos: root es owner, notebookum_user es grupo. Solo lectura (550) para codigo
RUN chown -R root:notebookum_user /app && \
    chmod -R 550 /app

# Exponer el puerto del microservicio
EXPOSE 5000

# Security: Correr la aplicacion como el usuario sin privilegios
USER notebookum_user

CMD ["uv", "run", "granian", "--interface", "wsgi", "main:app", "--host", "0.0.0.0", "--port", "5000", "--workers", "2"]