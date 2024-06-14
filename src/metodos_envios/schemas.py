from pydantic import BaseModel
from typing import Union

class Metodo_EnvioBase(BaseModel):
    nombre: str
    descripcion: Union[str, None] = None

class Metodo_EnvioCrear(Metodo_EnvioBase):
    pass

class Metodo_Envio(Metodo_EnvioBase):
    id: int

    class Config:
        orm_mode = True


