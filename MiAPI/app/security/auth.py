#Seguridad HTTP Basic
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
security= HTTPBasic()
def verificar_Peticion(credenciales:HTTPBasicCredentials=Depends(security)):# este es para que en caso de que haya un usuario correcto es el que se va a dejar que elimine
    userAuth = secrets.compare_digest(credenciales.username, "poñoñoin")
    passAuth = secrets.compare_digest(credenciales.password, "123456")

    if not(userAuth and passAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= "Credenciales no autorizadas"
        )
    return credenciales.username