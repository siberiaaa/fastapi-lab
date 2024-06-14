from pydantic import BaseModel
from typing import Union

class Estado_CaracteristicaBase(BaseModel):
    nombre: str
    descripcion: Union[str, None] = None

class Estado_CaracteristicaCrear(Estado_CaracteristicaBase):
    pass

class Estado_Caracteristica(Estado_CaracteristicaBase):
    id: int

    class Config:
        orm_mode = True


