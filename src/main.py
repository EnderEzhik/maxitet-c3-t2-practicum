from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from src.routes import mods, versions, categories, auth, users


app = FastAPI(title="EasyMods")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(mods.router)
app.include_router(versions.router)
app.include_router(categories.router)
app.include_router(auth.router)
app.include_router(users.router)


@app.get("/")
async def index():
    return FileResponse("static/index.html")
