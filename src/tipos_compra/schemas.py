from pydantic import BaseModel

class TipoBase(BaseModel):
    nombre: str
    descripcion: str | None = None

class Tipo_Usuario(TipoBase):
    pass

class Tipo_Usuario(TipoBase):
    id: int

    class Config:
        orm_mode = True

