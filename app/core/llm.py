import os
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv

load_dotenv()

def get_main_llm():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️ AVISO: OPENAI_API_KEY no encontrada. El bot fallará al intentar pensar.")
    
    return ChatOpenAI(
        model="gpt-4o-mini", 
        temperature=0,
        streaming=True
    )

def get_reasoning_llm():
    return ChatAnthropic(
        model="claude-3-5-sonnet-20240620",
        temperature=0
    )