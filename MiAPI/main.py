#importaciones
from fastapi import FastAPI
import asyncio
from typing import Optional

#instancia del servidor
app = FastAPI(
     tittle="Mi primer API",
     description="Poñoñoin",
     version="1.0.0")

usuarios = [
     {"id":1, "nombre":"Juan", "edad":"21"},
     {"id":2, "nombre":"Israel", "edad":"20"},
     {"id":3, "nombre":"Yael", "edad":"19"},
]

#Endpoints
@app.get("/", tags=["Inicio"])
async def bienvenida():
     return {"mensaje": "Bienvenido a mi API!"}

@app.get("/HolaMundo", tags=["Bienvenida Asincrona"])
async def Hola():
     await asyncio.sleep(3) #simulacion de peticion
     return {
          "mensaje": "Hola mundo FastAPI!" ,
          "estatus":"200"}   
 
@app.get("/v1/usuario/{id}", tags=["Parametro obligatorio"])
async def consultaUno (id: int):
     return {"Se encontro usuario":id}

@app.get("/v1/usuarios/", tags=["Parametro opcional"])
async def consultaTodos (id: Optional [int] = None):
    if id is not None:
         for usuario in usuarios:
          if usuario["id"] == id:
              return {"mensaje": "usuario encontrado", "usuario": usuario}
          return {"mensaje": "usuario no encontrado", "usuario":id}
         else:
             return {"mensaje": "No se proporciono id"}
