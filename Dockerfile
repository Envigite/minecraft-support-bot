FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema (necesarias para compilar psycopg/asyncpg a veces)
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Instalar Poetry (opcional, si usas pip puedes saltar esto)
RUN pip install poetry

# Copiar archivos de dependencias
COPY pyproject.toml poetry.lock* /app/

# Instalar dependencias (sin crear virtualenv dentro del container)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copiar el código
COPY . /app

# El comando se define en docker-compose, pero dejamos un default
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]