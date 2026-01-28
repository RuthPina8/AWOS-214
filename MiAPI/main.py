#importaciones
from fastapi import FastAPI
import asyncio

#instancia del servidor
app = FastAPI()

#Endpoints
@app.get("/")
async def bienvenida():
     return {"mensaje": "Bienvenido a mi API!"}

@app.get("/HolaMundo")
async def Hola():
     await asyncio.sleep(3) #simulacion de peticion
     return {
          "mensaje": "Hola mundo FastAPI!" ,
          "estatus":"200"}    