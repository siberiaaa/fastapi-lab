from pydantic import BaseModel
from datetime import datetime

class CompraBase(BaseModel):
    cantidad: int
    fecha: datetime | None = None
    cliente_cedula: str
    producto_id: int
    tipo_compra_id: int
    estado_compra_id: int | None = None

class CompraCrear(CompraBase):
    pass

class Compra(CompraBase):
    id: int

    class Config:
        orm_mode = True

