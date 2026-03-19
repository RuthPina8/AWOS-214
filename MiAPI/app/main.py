#importaciones
from fastapi import FastAPI
from app.routers import varios, usuarios

#instancia del servidor
app = FastAPI(
     title="Mi primer API",
     description="Poñoñoin",
     version="1.0.0"
     )

app.include_router(usuarios.router)
app.include_router(varios.router)
