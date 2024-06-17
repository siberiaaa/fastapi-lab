from pydantic import BaseModel

class CotizacionBase(BaseModel):
    precio: float
    compra_id: int
    estado_cotizacion_id: int

class CotizacionCrear(CotizacionBase):
    pass

class Cotizacion(CotizacionBase):
    id: int

    class Config:
        orm_mode = True

