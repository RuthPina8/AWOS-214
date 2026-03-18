#importaciones
from fastapi import Depends, FastAPI, status, HTTPException, Depends
import asyncio
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from fastapi.middleware.cors import CORSMiddleware


#instancia del servidor
app = FastAPI(
     title="Tienda de productos",
     description="API para gestionar productos en una tienda",
     version="1.0.0"
     )
  
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Simulacion de DB
productos = [
    {"id": 1, "nombre": "Papel higiénico", "precio": 28.0, "stock": 15, "categoria": "Limpieza"},
    {"id": 2, "nombre": "Pasta Spaghetti", "precio": 20.0, "stock": 20, "categoria": "Alimentos"},
]

#modelo de validacion
class producto (BaseModel):
    id: int = Field(..., gt=0, description="Identificador del producto")
    nombre: str = Field(..., min_length=2, max_length=60, example="Juan Pérez")
    precio: float = Field(..., gt=0, description="Precio del producto, debe ser mayor a 0")
    stock: int = Field(..., ge=0, description="Cantidad de productos en stock, debe ser mayor o igual a 0")
    categoria: str = Field(..., min_length=3, max_length=50, example="Electrónica")

class producto_delete(BaseModel):
    id: int = Field (..., gt=0, description="identificador de producto")

#Seguridad HTTP Basic
security= HTTPBasic()
def verificar_Peticion(credenciales:HTTPBasicCredentials=Depends(security)):# este es para que en caso de que haya un usuario correcto es el que se va a dejar que elimine
    userAuth = secrets.compare_digest(credenciales.username, "ruth")
    passAuth = secrets.compare_digest(credenciales.password, "123456")

    if not(userAuth and passAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= "Credenciales no autorizadas"
        )
    return credenciales.username
#Endpoints

@app.get("/", tags=["Inicio"])
async def bienvenida():
     return {"mensaje": "¡Bienvenido a la tienda de productos!"}

@app.get("/HolaMundo", tags=["Bienvenida Asincrona"])
async def Hola():
     await asyncio.sleep(3) #simulacion de peticion
     return {
          "mensaje": "Hola mundo FastAPI!" ,
          "estatus":"200"}   
#Lista de productos
@app.get("/v1/product/", tags=["CRUD HTTP"])
async def lista_productos():
    return productos
#Consultar un producto por su ID
@app.get("/v1/paramentroOb/{id}", tags=["Parametro obligatorio"])
async def consultaUno (id: int):
     return {"Se encontro el producto":id}

#Agregar un nuevo producto
@app.post("/v1/product/", tags=["CRUD HTTP"], status_code=status.HTTP_201_CREATED)
async def crear_producto(producto: producto):
    for p in productos:
        if p["id"] == producto.id:
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
    productos.append(producto.dict())  
    return {
        "mensaje": "Producto agregado",
        "Producto": producto
    }   
#actualizar un producto
@app.put("/v1/products/{id}", tags=["CRUD HTTP"], status_code=status.HTTP_204_NO_CONTENT)#actualizar
async def actualizar_producto(id: int, producto: producto):
     for p in productos:
         if p["id"] == id:
             p.update(producto.dict())
             return
     raise HTTPException(
          status_code=404,
          detail="Producto no encontrado"
     )

@app.delete("/v1/products/{id}", tags=["CRUD HTTP"], status_code=status.HTTP_200_OK)
async def eliminar_producto(id: int,userAuth:str= Depends(verificar_Peticion)):
    for index, usr in enumerate(productos):
        if usr["id"] == id:
            productos.pop(index)
            return {"mensaje": f"Producto eliminado correctamente {userAuth}"}
        #si no encontramos  el usuario mandamos error 404, como se platico
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
            )
