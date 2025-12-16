import json
from langchain_core.messages import SystemMessage, ToolMessage

from app.graph.state import AgentState
from app.graph.tools_adapter import create_checkout_tools
from app.core.llm import get_main_llm

SYSTEM_PROMPT = """Eres un asistente experto del E-commerce 'Minecraft Store'.
Tu objetivo es ayudar a los usuarios a encontrar items y revisar sus pedidos.

Reglas:
1. Si te preguntan precios o stock, SIEMPRE usa la herramienta 'search_products'. NO inventes datos.
2. Si te preguntan por un pedido, usa 'get_user_orders'.
3. Sé amable y usa emojis relacionados con Minecraft (💎, ⚔️, 📦).
4. Si no encuentras información, dilo honestamente.
"""

# --- NODO: LLAMAR AL MODELO ---
async def call_model(state: AgentState, config):
    # 1. Se recupera la sesión de DB que se inyectará desde la API
    session = config["configurable"]["db_session"]
    
    # 2. Se crean las herramientas con esa sesión
    tools = create_checkout_tools(session)
    
    # 3. Se inicializa el LLM y le "atamos" (bind), Si no hago esto → la IA NO puede usar tools
    llm = get_main_llm()
    llm_with_tools = llm.bind_tools(tools)
    
    # 4. Se construye el historial de mensajes
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    
    # 5. Se invoca al modelo
    response = await llm_with_tools.ainvoke(messages)
    
    # 6. Se retorna la actualización del estado (nuevo mensaje)
    return {"messages": [response]}

# --- NODO: EJECUTAR HERRAMIENTAS ---
async def run_tools(state: AgentState, config):
    print("🔧 Ejecutando herramientas manualmente...")
    
    # 1. Se recupera la sesión y las tools
    session = config["configurable"]["db_session"]
    tools = create_checkout_tools(session)
    
    # 2. Se convierte la lista de tools a un diccionario para buscar rápido
    # Ejemplo: { "search_products": <funcion>, "get_user_orders": <funcion> }
    tools_by_name = {t.name: t for t in tools}
    
    # 3. Se obtiene el último mensaje de la IA (que contiene la solicitud de tool)
    last_message = state["messages"][-1]
    
    # 4. Preparamos una lista para guardar los resultados
    results = []
    
    # 5. Se itera sobre cada solicitud (la IA puede pedir varias cosas a la vez)
    for tool_call in last_message.tool_calls:
        name = tool_call["name"]
        args = tool_call["args"]
        call_id = tool_call["id"]
        
        # Se busca la tool
        tool = tools_by_name.get(name)
        
        if tool:
            print(f"   👉 Ejecutando {name} con args: {args}")
            # Se ejecuta la herramienta (ainvoke es la forma async de llamar)
            result_content = await tool.ainvoke(args)
        else:
            result_content = f"Error: La herramienta '{name}' no existe."
            
        # Se crea el mensaje de respuesta (ToolMessage)
        # Esto es lo que la IA necesita leer para saber qué pasó
        results.append(
            ToolMessage(
                content=str(result_content),
                tool_call_id=call_id,
                name=name
            )
        )
        
    # Retornamos los mensajes nuevos para agregarlos al historial
    return {"messages": results}