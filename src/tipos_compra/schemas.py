from pydantic import BaseModel
from typing import Union

class Tipo_CompraBase(BaseModel):
    nombre: str
    descripcion: Union[str, None] = None

class Tipo_CompraCrear(Tipo_CompraBase):
    pass

class Tipo_Compra(Tipo_CompraBase):
    id: int

    class Config:
        orm_mode = True


