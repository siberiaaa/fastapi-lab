from typing import Generic, Optional, TypeVar, Union
from pydantic import BaseModel

from pydantic.generics import GenericModel

DataT = TypeVar('DataT')

class Respuesta(GenericModel, Generic[DataT]):
    ok: bool
    mensaje: str
    data: Optional[DataT] = None

class Token(BaseModel): 
    usuario : str
    token_acceso : str
    tipo_token : str

class DataToken(BaseModel): 
    cedula: str
    nombre_completo: str
    tipo_usuario_id: int