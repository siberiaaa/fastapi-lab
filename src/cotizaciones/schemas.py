from pydantic import BaseModel
from typing import Union

import compras.schemas as producto_schema

class CotizacionBase(BaseModel):
    precio: float
    compra_id: int
    estado_cotizacion_id: Union[int, None] = None

class CotizacionCrear(CotizacionBase):
    pass

class Cotizacion(CotizacionBase):
    id: int

    class Config:
        orm_mode = True

