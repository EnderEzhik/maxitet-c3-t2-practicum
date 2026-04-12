from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes import mods, versions, categories


app = FastAPI(title="EasyMods")

origins = [
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(mods.router)
app.include_router(versions.router)
app.include_router(categories.router)


@app.get("/")
async def index():
    return { "message": "api is work" }
