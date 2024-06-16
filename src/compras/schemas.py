from pydantic import BaseModel
from datetime import datetime

class CompraBase(BaseModel):
    cantidad: int
    fecha: datetime
    cliente_cedula: str
    producto_id: int
    tipo_compra_id: int
    estado_compra_id: int

class CompraCrear(CompraBase):
    pass

class Compra(CompraBase):
    id: int

    class Config:
        orm_mode = True

