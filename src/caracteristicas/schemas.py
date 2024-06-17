from pydantic import BaseModel

class CaracteristicaBase(BaseModel):
    nombre: str
    explicacion: str
    encargo_id: int
    estado_caracteristica_id: int

class CaracteristicaCrear(CaracteristicaBase):
    pass

class Caracteristica(CaracteristicaBase):
    id: int

    class Config:
        orm_mode = True

