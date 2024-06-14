from pydantic import BaseModel
from typing import Union
from datetime import datetime

class UsuarioBase(BaseModel):
    cedula: str
    nombres: str
    apellidos: str
    nacimiento: datetime
    direccion: str
    correo: str
    contraseña: str
    tipo_id: int

class UsuarioCrear(UsuarioBase):
    pass

class Usuario(UsuarioBase):

    class Config:
        orm_mode = True


