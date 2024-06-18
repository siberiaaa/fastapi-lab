from pydantic import BaseModel
from typing import Union

class CaracteristicaBase(BaseModel):
    nombre: str
    explicacion: str
    encargo_id: int
    estado_caracteristica_id: Union[int, None] = None

class CaracteristicaCrear(CaracteristicaBase):
    pass

class Caracteristica(CaracteristicaBase):
    id: int

    class Config:
        orm_mode = True

