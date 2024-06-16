from pydantic import BaseModel
from datetime import datetime

class ReseñaBase(BaseModel):
    invencion: datetime
    inventor: str
    años_produccion: float
    producto_id: int

class ReseñaCrear(ReseñaBase):
    pass

class Reseña(ReseñaBase):
    id: int

    class Config:
        orm_mode = True


