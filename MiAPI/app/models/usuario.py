#modelo de validacion
from pydantic import BaseModel, Field
class usuario_create (BaseModel):
    id: int = Field(..., gt=0, description="Identificador de usuario")
    nombre: str = Field(..., min_length=3, max_length=50, example="Juan Pérez")
    edad: int = Field(..., ge=1, le=123, description="Edad valida entr 1 y 123")
