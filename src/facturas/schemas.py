from pydantic import BaseModel
from datetime import datetime

class FacturaBase(BaseModel):
    fecha_entrega: datetime
    cotizacion_id: int
    metodo_envio_id: int
    metodo_pago_id: int

class FacturaCrear(FacturaBase):
    pass

class Factura(FacturaBase):
    id: int

    class Config:
        orm_mode = True

