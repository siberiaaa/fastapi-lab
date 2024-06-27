from pydantic import BaseModel
from typing import Union
from datetime import datetime

from productos import schemas as producto_schema
class CompraBase(BaseModel):
    cantidad: int
    fecha: Union[datetime, None] = None
    cliente_cedula: str
    producto_id: int
    tipo_compra_id: int
    estado_compra_id: Union[int, None] = None

class CompraCrear(CompraBase):
    pass

class CompraInfo(CompraBase):
    producto: producto_schema.Producto

class Compra(CompraBase):
    id: int

    class Config:
        orm_mode = True

