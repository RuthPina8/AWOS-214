from fastapi import HTTPException, status, Depends, APIRouter
from app.models.usuario import usuario_create
from app.data.database import usuarios
from app.security.auth import verificar_Peticion

router= APIRouter(
    prefix="/v1/usuarios", tags= ["CRUD HTTP"]
)


@router.get("/")
async def leer_usuario ():
     return {
         "status": "200",
         "total": len(usuarios),
         "usuarios": usuarios
     }

@router.post("/", status_code=status.HTTP_201_CREATED)#agregar
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
