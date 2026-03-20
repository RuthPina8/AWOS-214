# importaciones
from fastapi import Depends, FastAPI, status, HTTPException
import asyncio
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt

# CONFIGURACION JWT / OAuth2
SECRET_KEY = "clave_super_secreta_poñoñoin_2024"   
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30                    
# usuario "de base de datos" 
USUARIO_DB = {
    "username": "poñoñoin",
    "password": "123456"
}

# esquema OAuth2 - le dice a FastAPI donde esta el endpoint de login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/login")

# INSTANCIA DEL SERVIDOR
app = FastAPI(
    title="Mi primer API",
    description="Poñoñoin - ahora con JWT",
    version="2.0.0"
)

# Configuracion de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DATOS EN NUESTRA DB
usuarios = [
    {"id": 1, "nombre": "Juan",   "edad": "21"},
    {"id": 2, "nombre": "Israel", "edad": "20"},
    {"id": 3, "nombre": "Yael",   "edad": "19"},
]

# MODELOS DE VALIDACION
class usuario_create(BaseModel):
    id:     int = Field(..., gt=0,          description="Identificador de usuario")
    nombre: str = Field(..., min_length=3, max_length=50, example="Juan Pérez")
    edad:   int = Field(..., ge=1, le=123,  description="Edad valida entre 1 y 123")

class usuario_delete(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de usuario")

class Token(BaseModel):
    access_token: str
    token_type:   str

# FUNCIONES JWT
def crear_token(data: dict, expires_delta: timedelta = None) -> str:
    """Genera un JWT firmado con expiracioon especifica"""
    payload = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    payload.update({"exp": expire})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verificar_token(token: str = Depends(oauth2_scheme)) -> str:
    """
    Dependencia que valida el JWT recibido en el header Authorization.
    Lanza 401 si el token es invalido o ha expirado
    """
    credencial_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credencial_exception
        return username
    except JWTError:
        raise credencial_exception

# ENDPOINT DE LOGIN  (genera el token)
@app.post("/v1/login", response_model=Token, tags=["Autenticacion OAuth2"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Recibe username + password (form).
    Si son correctos devuelve un JWT valido por 30 minutos.
    """
    if (form_data.username != USUARIO_DB["username"] or
            form_data.password != USUARIO_DB["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = crear_token(
        data={"sub": form_data.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": token, "token_type": "bearer"}

# ENDPOINTS

@app.get("/", tags=["Inicio"])
async def bienvenida():
    return {"mensaje": "Bienvenido a mi API con JWT!"}


@app.get("/HolaMundo", tags=["Bienvenida Asincrona"])
async def Hola():
    await asyncio.sleep(3)
    return {"mensaje": "Hola mundo FastAPI!", "estatus": "200"}


@app.get("/v1/paramentroOb/{id}", tags=["Parametro obligatorio"])
async def consultaUno(id: int):
    return {"Se encontro usuario": id}


@app.get("/v1/parametroOp/", tags=["Parametro opcional"])
async def consultaTodos(id: Optional[int] = None):
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return {"mensaje": "usuario encontrado", "usuario": usuario}
        return {"mensaje": "usuario no encontrado", "usuario": id}
    return {"mensaje": "No se proporciono id"}


@app.get("/v1/usuarios/", tags=["CRUD HTTP"])
async def leer_usuario():
    return {
        "status": "200",
        "total": len(usuarios),
        "usuarios": usuarios
    }


@app.post("/v1/usuarios/", tags=["CRUD HTTP"], status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario: usuario_create):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(status_code=400, detail="El id ya existe")
    usuarios.append(usuario.dict())
    return {"mensaje": "Usuario agendado", "Usuario": usuario}


# PUT  protegido con JWT 
@app.put("/v1/usuarios/", tags=["CRUD HTTP"], status_code=status.HTTP_204_NO_CONTENT)
async def actualizar_usuario(
    usuario: dict,
    current_user: str = Depends(verificar_token)
):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            if "nombre" in usuario:
                usr["nombre"] = usuario["nombre"]
            if "edad" in usuario:
                usr["edad"] = usuario["edad"]
            return
    raise HTTPException(status_code=404, detail="Usuario no encontrado")


#   DELETE  protegido con JWT 
@app.delete("/v1/usuarios/{id}", tags=["CRUD HTTP"], status_code=status.HTTP_200_OK)
async def eliminar_usuario(
    id: int,
    current_user: str = Depends(verificar_token)
):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios.pop(index)
            return {"mensaje": f"Usuario eliminado correctamente por: {current_user}"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")