#importaciones
from fastapi import FastAPI
from app.routers import varios, usuarios
from app.data.db import  engine
from app.data import usuario 

usuario.Base.metadata.create_all(bind=engine)

#instancia del servidor
app = FastAPI(
     title="Mi primer API",
     description="Poñoñoin",
     version="1.0.0"
     )

app.include_router(usuarios.router)
app.include_router(varios.router)
