from pydantic import BaseModel
from typing import Union

class CategoriaBase(BaseModel):
    nombre: str
    descripcion: Union[str, None] = None

class CategoriaCrear(CategoriaBase):
    pass

class Categoria(CategoriaBase):
    id: int

    class Config:
        orm_mode = True

