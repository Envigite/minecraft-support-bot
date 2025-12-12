from fastapi import FastAPI

app = FastAPI(title="Minecraft AI Support")

@app.get("/health")
async def health_check():
    return {"status": "ok", "system": "ready_to_rock"}