import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator
from dotenv import load_dotenv

load_dotenv()

# Recuperamos la URL correcta del .env
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("❌ FATAL: DATABASE_URL no está configurada en .env")

# Aplicamos el fix de SSL para Neon/Asyncpg
engine = create_async_engine(
    DATABASE_URL,
    echo=False, # True para ver cada query SQL en la consola (útil para debug)
    connect_args={"ssl": "require"}
)

# Fábrica de Sesiones
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependencia para FastAPI (Inyeccion de Dependencias)
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()