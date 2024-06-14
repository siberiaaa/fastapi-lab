from pydantic import BaseModel
from typing import Union

class Tipo_UsuarioBase(BaseModel):
    nombre: str
    descripcion: Union[str, None] = None

class Tipo_UsuarioCrear(Tipo_UsuarioBase):
    pass

class Tipo_Usuario(Tipo_UsuarioBase):
    id: int

    class Config:
        orm_mode = True


