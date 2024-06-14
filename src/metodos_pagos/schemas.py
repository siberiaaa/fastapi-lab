from pydantic import BaseModel
from typing import Union

class Metodo_PagoBase(BaseModel):
    nombre: str
    descripcion: Union[str, None] = None

class Metodo_PagoCrear(Metodo_PagoBase):
    pass

class Metodo_Pago(Metodo_PagoBase):
    id: int

    class Config:
        orm_mode = True


