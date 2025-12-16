from fastapi import FastAPI
from app.api.v1.chat import router as chat_router

app = FastAPI(title="Minecraft AI Support")

# Registramos el router con un prefijo
# Ahora tu endpoint será accesible en: POST /api/v1/chat
app.include_router(chat_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "ok", "system": "ready_to_rock"}