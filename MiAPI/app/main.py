#importaciones
from fastapi import FastAPI, status, HTTPException
import asyncio
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

#instancia del servidor
app = FastAPI(
     title="Mi primer API",
     description="Poñoñoin",
     version="1.0.0"
     )
# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
usuarios = [
     {"id":1, "nombre":"Juan", "edad":"21"},
     {"id":2, "nombre":"Israel", "edad":"20"},
     {"id":3, "nombre":"Yael", "edad":"19"},
]
#modelo de validacion
class usuario_create (BaseModel):
    id: int = Field(..., gt=0, description="Identificador de usuario")
    nombre: str = Field(..., min_length=3, max_length=50, example="Juan Pérez")
    edad: int = Field(..., ge=1, le=123, description="Edad valida entr 1 y 123")
    

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
 
@app.get("/v1/paramentroOb/{id}", tags=["Parametro obligatorio"])
async def consultaUno (id: int):
     return {"Se encontro usuario":id}

@app.get("/v1/parametroOp/", tags=["Parametro opcional"])
async def consultaTodos (id: Optional [int] = None):
    if id is not None:
         for usuario in usuarios:
          if usuario["id"] == id:
              return {"mensaje": "usuario encontrado", "usuario": usuario}
          return {"mensaje": "usuario no encontrado", "usuario":id}
         else:
             return {"mensaje": "No se proporciono id"}


@app.get("/v1/usuarios/", tags=["CRUD HTTP"])
async def leer_usuario ():
     return {
         "status": "200",
         "total": len(usuarios),
         "usuarios": usuarios
     }

@app.post("/v1/usuarios/", tags=["CRUD HTTP"], status_code=status.HTTP_201_CREATED)#agregar
async def crear_usuario(usuario: usuario_create):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
    usuarios.append(usuario.dict())  
    return {
        "mensaje": "Usuario agendado",
        "Usuario": usuario
    }   


@app.put("/v1/usuarios/", tags=["CRUD HTTP"], status_code=status.HTTP_204_NO_CONTENT)#actualizar
async def actualizar_usuario (usuario: dict):# senececista usuario coon diccionario
     for usr in usuarios:# con base a los datos obtenidos modificar con el id para hacer el cambio
         if usr ["id"] == usuario.get("id"):
             if "nombre" in usuario:
                 usr["nombre"] = usuario["nombre"]
             if "edad" in usuario:
                 usr["edad"] = usuario["edad"]
             return

     raise HTTPException(
          status_code=404,
          detail="Usuario no encontrado"
     )


@app.delete("/v1/usuarios/{id}", tags=["CRUD HTTP"], status_code=status.HTTP_200_OK)
async def eliminar_usuario(id: int):
     for usr in usuarios:#recibimos el id del usuario que queremos eliminar
          if usr["id"] == id:#aqui checamos si el id coincide con alguno de la lista
               usuarios.remove(usr)  #si lo encontramos lo elimina de la lista
               return {
                    "mensaje": "Usuario eliminado correctamente",
                    "usuario": usr
               }
     
     #si no encontramos  el usuario mandamos error 404, como se platico
     raise HTTPException(
          status_code=404,
          detail="Usuario no encontrado"
     )
