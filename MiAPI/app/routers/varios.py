#Endpoints varios
from typing import Optional
import asyncio
from app.data.database import usuarios
from fastapi import APIRouter

router = APIRouter (tags=['Varios'])
@router.get("/",)
async def bienvenida():
     return {"mensaje": "Bienvenido a mi API!"}

@router.get("/HolaMundo")
async def Hola():
     await asyncio.sleep(3) #simulacion de peticion
     return {
          "mensaje": "Hola mundo FastAPI!" ,
          "estatus":"200"}   
 
@router.get("/v1/paramentroOb/{id}" )
async def consultaUno (id: int):
     return {"Se encontro usuario":id}

@router.get("/v1/parametroOp/")
async def consultaTodos (id: Optional [int] = None):
    if id is not None:
         for usuario in usuarios:
          if usuario["id"] == id:
              return {"mensaje": "usuario encontrado", "usuario": usuario}
          return {"mensaje": "usuario no encontrado", "usuario":id}
         else:
             return {"mensaje": "No se proporciono id"}