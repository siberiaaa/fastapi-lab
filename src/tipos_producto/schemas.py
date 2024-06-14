from pydantic import BaseModel
from typing import Union

class Tipo_ProductoBase(BaseModel):
    nombre: str
    descripcion: Union[str, None] = None
    funcionalidad: bool

class Tipo_ProductoCrear(Tipo_ProductoBase):
    pass

class Tipo_Producto(Tipo_ProductoBase):
    id: int

    class Config:
        orm_mode = True


