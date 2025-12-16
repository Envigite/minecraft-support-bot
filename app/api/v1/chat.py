from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from langchain_core.messages import HumanMessage

from app.core.database import get_db
from app.graph.workflow import app_graph

router = APIRouter()

# Esto define como debe venir el JSON
class ChatRequest(BaseModel):
    message: str
    email: str = "invitado@minecraft.com"

# --- EL ENDPOINT ---
@router.post("/chat")
async def chat_endpoint(
    request: ChatRequest, 
    # Inyección de Dependencias: FastAPI da la sesión de DB segura
    db: AsyncSession = Depends(get_db) 
):
    try:
        # 1. Se crea el estado inicial del afente, parte con lo que dijo el usuario
        inputs = {
            "messages": [HumanMessage(content=request.message)],
            "user_email": request.email
        }

        # 2. Se pasa la sesión DB al grafo (para que la usen los nodos)
        config = {"configurable": {"db_session": db}}

        # 3. Ejecutamos el Grafo
        result = await app_graph.ainvoke(inputs, config)

        # 4. Se extrae la última respuesta de la IA
        last_message = result["messages"][-1]
        
        return {
            "response": last_message.content,
            "tool_used": len(result["messages"]) > 2 # Me indica si usó tools
        }

    except Exception as e:
        print(f"❌ Error en el chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))