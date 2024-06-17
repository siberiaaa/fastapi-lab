from typing import Generic, Optional, TypeVar

from pydantic.generics import GenericModel

DataT = TypeVar('DataT')

class Respuesta(GenericModel, Generic[DataT]):
    ok: bool
    mensaje: str
    data: Optional[DataT] = None
