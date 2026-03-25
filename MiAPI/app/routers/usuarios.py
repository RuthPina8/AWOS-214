from fastapi import HTTPException, status, Depends, APIRouter
from app.models.usuario import usuario_create
from app.data.database import usuarios
from app.security.auth import verificar_Peticion

from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuario import Usuario as usuarioDB

router= APIRouter(
    prefix="/v1/usuarios", tags= ["CRUD HTTP"]
)


@router.get("/")
async def leer_usuario (db: Session = Depends(get_db)):
     
     queryUsers = db.query(usuarioDB).all()

     return {
         "status": "200",
         "total": len(queryUsers),
         "usuarios": queryUsers
     }

@router.post("/", status_code=status.HTTP_201_CREATED)#agregar
async def crear_usuario(usuarioP: usuario_create, db: Session = Depends(get_db)):
    nuevo_usuario = usuarioDB(nombre=usuarioP.nombre, edad=usuarioP.edad)
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return {
        "mensaje": "Usuario agendado",
        "Usuario": usuarioP
    }   


@router.put("/{id}", status_code=status.HTTP_204_NO_CONTENT)#actualizar
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


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def eliminar_usuario(id: int,userAuth:str= Depends(verificar_Peticion)):
     for index, usr in enumerate (usuarios):#recibimos el id del usuario que queremos eliminar
          if usr["id"] == id:#aqui checamos si el id coincide con alguno de la lista
            usuario_eliminado = usuarios.pop(index)#si lo encontramos lo elimina de la lista
            return { "mensaje": f"Usuario eliminado correctamente{userAuth}"}
          return{"mensaje": "Usuario no encontrado", "id": id}
                    
            
     
     #si no encontramos  el usuario mandamos error 404, como se platico
     raise HTTPException(
          status_code=404,
          detail="Usuario no encontrado"
     )
