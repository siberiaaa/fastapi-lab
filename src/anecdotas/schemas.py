from pydantic import BaseModel

class AnecdotaBase(BaseModel):
    nombre: str
    descripcion: str
    años_produccion: float
    reseña_id: int

class AnecdotaCrear(AnecdotaBase):
    pass

class Anecdota(AnecdotaBase):
    id: int

    class Config:
        orm_mode = True

