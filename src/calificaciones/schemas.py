from pydantic import BaseModel, field_validator
from typing import Union
class CalificacionBase(BaseModel):
    titulo: str
    comentario: str
    estrellas: int
    emoticono: Union[str, None] = None
    usuario_cedula: str
    producto_id: int

    @field_validator('estrellas')
    def verificar_estrellas(cls, estrellas): 
        if estrellas > 5: 
            raise ValueError('El máximo de estrellas es 5')
        if estrellas < 0: 
            raise ValueError('El mínimo de estrellas es 0. ¡No seas cruel!')
        return estrellas

class CalificacionCrear(CalificacionBase):
    pass

class Calificacion(CalificacionBase):
    id: int

    class Config:
        orm_mode = True


