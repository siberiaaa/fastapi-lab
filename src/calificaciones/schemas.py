from pydantic import BaseModel
from typing import Union

class CalificacionBase(BaseModel):
    titulo: str
    comentario: str
    estrellas: int
    emoticono: Union[str, None] = None
    usuario_cedula: str
    producto_id: int

class CalificacionCrear(CalificacionBase):
    pass

class Calificacion(CalificacionBase):
    id: int

    class Config:
        orm_mode = True


