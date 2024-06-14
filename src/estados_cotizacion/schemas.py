from pydantic import BaseModel
from typing import Union

class Estado_CotizacionBase(BaseModel):
    nombre: str
    descripcion: Union[str, None] = None

class Estado_CotizacionCrear(Estado_CotizacionBase):
    pass

class Estado_Cotizacion(Estado_CotizacionBase):
    id: int

    class Config:
        orm_mode = True


