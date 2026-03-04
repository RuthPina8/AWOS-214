from datetime import datetime
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field
from typing import Literal # solo nos va a permitir ciertos valores especificos que en nuestro caso es para el estado del libro, si es disponible o prestado 

libros = []
prestamos = []

app = FastAPI(
     title="Repaso de FastAPI",
     description="API para practicar FastAPI y sus componentes",
     version="1.0.0"
     )

#modelo de validacion
class libroRegister (BaseModel):
    id: int = Field(..., gt=0, description="Identificador del libro")
    nombreLibro: str = Field(..., min_length=3, max_length=100, example="Nombre del Libro")
    anio: int = Field(..., gt=1450, le=datetime.now().year, description="Año mayor a 1450 y menor o igual al actual")#datetime utilizado para tomar el año actual y evitar que se ingresen años futuros
    paginas: int = Field(..., gt=1, description="Número de páginas del libro mayor a 1")
    estado: Literal["disponible", "prestado"] 
   
#registro libros
@app.post("/v1/libros/", tags=["CRUD HTTP"], status_code=status.HTTP_201_CREATED)#agregar
async def registrar_libro(libro: libroRegister):
    for libro_guardado in libros:
        if libro_guardado["id"] == libro.id:
            raise HTTPException(
                status_code=409,
                detail="El id ya existe"
            )
    libros.append(libro.dict())  
    return {
        "mensaje": "Libro registrado con éxito",
        "Libro": libro
    }    

#lista libros disponibles
@app.get("/v1/libros/", tags=["CRUD HTTP"])
async def lista_libros():
    return libros

#Buscar un libro por su nombre
@app.get("/v1/libros/busqueda")
async def buscar_libro(nombre: str):# no se le ponen tags pq es un endpoint de busqueda y no de CRUD
    for libro in libros:
        if libro["nombreLibro"].lower() == nombre.lower():
            return {"mensaje": "Libro encontrado", "Libro": libro}
    raise HTTPException(
        status_code=404,
        detail="Libro no encontrado"
    )

#Registrar el préstamo de un libro a un usuario
@app.post("/v1/prestamos", status_code=201)
async def Registro_prestamo(id_libro: int, usuario: str):
    for libro in libros:
        if libro["id"] == id_libro:
            if libro["estado"] == "prestado":
                raise HTTPException(
                    status_code=409,
                    detail="Libro no disponible, ya está prestado"
                )
            libro["estado"] = "prestado"
            prestamo = {
                "id_libro": id_libro,
                "usuario": usuario
            }
            prestamos.append(prestamo)
            return {"mensaje": "El préstamo ha sido registrado con exito", "prestamo": prestamo}

    raise HTTPException(
        status_code=404,
        detail="El libro que buscas no ha sido encontrado"
    )

#Marcar un libro como devuelto
@app.put("/v1/prestamos/{id_libro}")
async def devolver_libro(id_libro: int):
    for prestamo in prestamos:
        if int(prestamo["id_libro"]) == int(id_libro):
            for libro in libros:
                if libro["id"] == id_libro:
                    libro["estado"] = "disponible"
            prestamos.remove(prestamo)  
            return {"mensaje": "el libro se ha devuelto correctamente"}
    raise HTTPException(
        status_code=404,
        detail="Este registro de préstamo no existe"
    )
#Eliminar el registro de un préstamo
@app.delete("/v1/prestamos/{id_libro}", tags=["CRUD HTTP"], status_code=status.HTTP_200_OK)
async def eliminar_prestamo(id_libro: int):
     for prestamo in prestamos:  #recibimos el id del libro que queremos eliminar del registro
          if prestamo["id_libro"] == id_libro:  #aqui checamos si el id coincide con alguno de la lista    
               # ponemos el libro como disponible otra vez
               for libro in libros:
                    if libro["id"] == id_libro:
                         libro["estado"] = "disponible"
               prestamos.remove(prestamo)  #si lo encontramos lo elimina de la lista
               return {
                    "mensaje": "Registro de préstamo eliminado correctamente",
                    "prestamo": prestamo
               }
     raise HTTPException(
          status_code=404,
          detail="Este registro de préstamo no existe"
     )