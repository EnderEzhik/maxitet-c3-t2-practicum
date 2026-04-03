from fastapi import FastAPI

from src.routes import mods, versions, categories


app = FastAPI(title="EasyMods")

app.include_router(mods.router)
app.include_router(versions.router)
app.include_router(categories.router)


@app.get("/")
async def index():
    return { "message": "api is work" }
