
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

# Usamos AsyncAttrs para compatibilidad total con async/await
class Base(AsyncAttrs, DeclarativeBase):
    pass