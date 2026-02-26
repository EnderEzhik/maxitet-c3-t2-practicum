from fastapi import FastAPI

from routes import mods


app = FastAPI()

app.include_router(mods.router)


@app.get("/")
async def index():
    return { "message": "api is work" }
