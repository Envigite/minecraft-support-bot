from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ecommerce import Product, Order, User 

async def search_products(query: str, session: AsyncSession) -> str:
    print(f"🛠️ TOOL CALL: Buscando productos con query='{query}'...")
    
    stmt = select(Product).where(
        (Product.name.ilike(f"%{query}%")) | 
        (Product.description.ilike(f"%{query}%"))
    ).limit(5)
    
    result = await session.execute(stmt)
    products = result.scalars().all()
    
    if not products:
        return "No encontré productos que coincidan con esa búsqueda."
    
    response_text = "Encontré estos productos:\n"
    for p in products:
        response_text += f"- {p.name} (Stock: {p.stock}): ${p.price}\n  Desc: {p.description}\n"
        
    return response_text

async def get_user_orders(email: str, session: AsyncSession) -> str:
    print(f"🛠️ TOOL CALL: Buscando órdenes para email='{email}'...")
    stmt = (
        select(Order)
        .join(Order.user)
        .where(User.email == email)
        .order_by(Order.created_at.desc())
        .limit(3)
    )
    
    result = await session.execute(stmt)
    orders = result.scalars().all()
    
    if not orders:
        return f"No encontré pedidos registrados para el email {email}."
    
    response_text = f"Pedidos recientes para {email}:\n"
    for o in orders:
        response_text += f"📦 Orden ID: {o.id} | Estado: {o.status} | Total: ${o.total_amount}\n"
        
    return response_text