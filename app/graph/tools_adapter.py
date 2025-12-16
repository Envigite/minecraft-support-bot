from typing import List
from langchain_core.tools import StructuredTool
from sqlalchemy.ext.asyncio import AsyncSession
from app.tools.ecommerce import search_products, get_user_orders

def create_checkout_tools(session: AsyncSession) -> List[StructuredTool]:
    
    async def _search_products_wrapper(query: str):
        return await search_products(query, session)
    
    tool_search = StructuredTool.from_function(
        func=None,
        coroutine=_search_products_wrapper,
        name="search_products",
        description="Útil para buscar items o productos en la tienda por nombre o descripción. Retorna precio, stock y detalles.",
    )

    # 2. Envolvemos 'get_user_orders'
    async def _get_user_orders_wrapper(email: str):
        return await get_user_orders(email, session)

    tool_orders = StructuredTool.from_function(
        func=None,
        coroutine=_get_user_orders_wrapper,
        name="get_user_orders",
        description="Útil para buscar el estado de los pedidos o historial de compras de un usuario dado su email.",
    )

    return [tool_search, tool_orders]