from pydantic import BaseModel
from typing import Union

class Estado_CompraBase(BaseModel):
    nombre: str
    descripcion: Union[str, None] = None

class Estado_CompraCrear(Estado_CompraBase):
    pass

class Estado_Compra(Estado_CompraBase):
    id: int

    class Config:
        orm_mode = True


