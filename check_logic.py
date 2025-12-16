import asyncio
from app.core.database import AsyncSessionLocal
from app.tools.ecommerce import search_products, get_user_orders

async def test_tools():
    print("🧪 INICIANDO TEST DE LÓGICA DE NEGOCIO...")
    
    async with AsyncSessionLocal() as session:
        # 1. Probar Búsqueda
        print("\n--- TEST 1: Buscar 'comida' ---")
        # Ajusta "espada" a algo que sepas que existe en tu DB, o usa un término genérico
        resultado_busqueda = await search_products("comida", session) 
        print(resultado_busqueda)
        
        # 2. Probar Búsqueda Fallida
        print("\n--- TEST 2: Buscar algo inexistente ---")
        resultado_fail = await search_products("iphone 15 pro max", session)
        print(resultado_fail)

        # 3. Probar Órdenes (Probablemente vacío, pero no debe dar error)
        print("\n--- TEST 3: Buscar órdenes ---")
        resultado_ordenes = await get_user_orders("usuario3@example.com", session)
        print(resultado_ordenes)
        if not resultado_ordenes:
            print("No se encontraron órdenes para usuario3@example.com")

    print("\n✅ TEST FINALIZADO")

if __name__ == "__main__":
    asyncio.run(test_tools())