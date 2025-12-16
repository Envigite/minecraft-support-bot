import asyncio
import os
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.models.ecommerce import Product, Order
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://admin:admin123@localhost:5432/minecraft_db")

async def check_database():
    print(f"🔌 Conectando a: {DATABASE_URL}")
    
    try:
        engine = create_async_engine(DATABASE_URL, echo=False)
        async_session = async_sessionmaker(engine, expire_on_commit=False)

        async with async_session() as session:
            # 1. Ping
            await session.execute(text("SELECT 1"))
            print("✅ Conexión establecida.")

            # 2. Verificar Productos
            print("🔍 Buscando productos...")
            products = (await session.execute(select(Product).limit(1))).scalars().first()
            if products:
                print(f"   -> Producto encontrado: {products.name} (ID: {products.id})")
            else:
                print("   -> Tabla products accesible, pero vacía.")

            # 3. Verificar Orders (La tabla nueva)
            print("🔍 Buscando tabla orders...")
            # Intentamos hacer un select simple para ver si la tabla existe y el modelo mapea bien
            try:
                orders = (await session.execute(select(Order).limit(1))).scalars().first()
                print("✅ Tabla 'orders' mapeada correctamente.")
            except Exception as e_order:
                print(f"❌ Error al leer 'orders'. ¿Ejecutaste el SQL de creación en DBeaver?\nError: {e_order}")

        await engine.dispose()
        print("\n🚀 DB CHECK FINALIZADO")

    except Exception as e:
        print("\n❌ ERROR CRÍTICO:")
        print(e)

if __name__ == "__main__":
    asyncio.run(check_database())