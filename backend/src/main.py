from fastapi import FastAPI

from src.routes import mods


app = FastAPI(title="EasyMods")

app.include_router(mods.router)


@app.get("/")
async def index():
    return { "message": "api is work" }
