from fastapi import Depends, FastAPI, status, HTTPException, Depends
import asyncio
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from fastapi.middleware.cors import CORSMiddleware
from typing import Literal


app = FastAPI(
     title="Examen 2do Parcial - AWOS-214",
     description="API para gestionar un Sistema de Tickets de Soporte Tecnico",
     version="1.0.0"
     )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tickets = [
    {"id": 1, "nombre": "Ruth Piña", "descripcion": "Solicitud ayuda con lap", "estado": "pendiente"},
    {"id": 2, "nombre": "Andre Martinez", "descripcion": "Cambio de equipo", "estado": "pendiente"},
    {"id": 3, "nombre": "Santiago Meneses", "descripcion": "Problema con impresora", "estado": "pendiente"},
    
]

class ticket (BaseModel):
    id: int = Field(..., gt=0, description="identificador de ticket")
    nombre: str = Field(..., min_length=5, max_length=60, example="Juan Pérez")
    descripcion: str = Field(..., min_length=3, max_length=50, example="Electrónica")
    estado: Literal["baja", "media", "alta"] = 'pendiente'

class ticket_delete(BaseModel):
    id: int = Field (..., gt=0, description="identificador de ticket")


security= HTTPBasic()
def verificar_Peticion(credenciales:HTTPBasicCredentials=Depends(security)):# este es para que en caso de que haya un usuario correcto es el que se va a dejar que elimine
    userAuth = secrets.compare_digest(credenciales.username, "soporte")
    passAuth = secrets.compare_digest(credenciales.password, "4321")

    if not(userAuth and passAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= "Credenciales no autorizadas"
        )
    return credenciales.username

@app.get("/", tags=["Inicio"])
async def bienvenida():
     return {"mensaje": "¡Bienvenido al examen del 2do parcial!"}

@app.get("/HolaMundo", tags=["Bienvenida Asincrona"])
async def Hola():
     await asyncio.sleep(3) 
     return {
          "mensaje": "holi!" ,
          "estatus":"200"}   

@app.post("/v1/ticket/", tags=["CRUD HTTP"], status_code=status.HTTP_201_CREATED)
async def crear_ticket(ticket: ticket):
    for t in tickets:
        if t["id"] == ticket.id:
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
    tickets.append(ticket.dict())  
    return {
        "mensaje": "Ticket creado",
        "Ticket": ticket
    } 

@app.get("/v1/ticket/", tags=["CRUD HTTP"])
async def lista_tickets():
    return tickets

@app.get("/v1/paramentroOb/{id}", tags=["Parametro obligatorio"])
async def ConsultaTicketPorID (id: int, userAuth:str= Depends(verificar_Peticion)):
     return {"Se encontro el ticket{userAuth}"}

#aqui
@app.put("/v1/ticket/{id_ticket}")
async def actualizar_estado(id_ticket: int, userAuth:str= Depends(verificar_Peticion)):
    for ticket in tickets:
        if int(ticket["id"]) == id_ticket:
            for ticket in tickets:
                if ticket["id"] == id_ticket:
                    if ticket["estado"] == "pendiente":
                        ticket["estado"] = "baja"
                    elif ticket["estado"] == "baja":
                        ticket["estado"] = "media"
                    elif ticket["estado"] == "media":
                        ticket["estado"] = "alta"
                    else:
                        ticket["estado"] = "pendiente"
                    return {"mensaje": f"Estado del ticket actualizado a {ticket['estado']} {userAuth}"}

        

@app.delete("/v1/tickets/{id}", tags=["CRUD HTTP"], status_code=status.HTTP_200_OK)
async def eliminar_ticket(id: int,userAuth:str= Depends(verificar_Peticion)):
    for index, usr in enumerate(tickets):
        if usr["id"] == id:
            tickets.pop(index)
            return {"mensaje": f"Ticket eliminado correctamente {userAuth}"}
        raise HTTPException(
            status_code=404,
            detail="Ticket no encontrado"
            )


