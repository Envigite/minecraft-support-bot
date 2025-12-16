import os
import asyncio
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

load_dotenv()

async def check_ai():
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ ERROR: No encontré la variable OPENAI_API_KEY en el archivo .env")
        return

    print(f"🔑 Llave detectada (comienza con): {api_key[:7]}...")
    print("🧠 Conectando con GPT-4o-mini (El modelo más económico)...")

    try:
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        
        mensaje = [HumanMessage(content="Responde solo con la palabra: FUNCIONANDO")]
        
        respuesta = await llm.ainvoke(mensaje)
        
        print("\n🤖 Respuesta de la IA:")
        print(f"   '{respuesta.content}'")
        print("\n✅ ¡CONEXIÓN EXITOSA! El cerebro está listo.")

    except Exception as e:
        print("\n❌ ERROR AL CONECTAR CON OPENAI:")
        print(e)
        print("Posibles causas: Saldo insuficiente (créditos agotados) o llave incorrecta.")

if __name__ == "__main__":
    asyncio.run(check_ai())