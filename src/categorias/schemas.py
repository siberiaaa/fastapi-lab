from pydantic import BaseModel

class CategoriaBase(BaseModel):
    nombre: str
    descripcion: str | None = None

class CategoriaCrear(CategoriaBase):
    pass

class Categoria(CategoriaBase):
    id: int

    class Config:
        orm_mode = True


