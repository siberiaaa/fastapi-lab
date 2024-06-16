from pydantic import BaseModel

class ProductoBase(BaseModel):
    nombre: str
    descripcion: str
    altura_cm: float
    anchura_cm: float
    profundidad_cm: float
    imagen: bytes
    peso_gramo: float
    usuario_cedula: str
    tipo_producto_id: int
    categoria_id: int

class ProductoCrear(ProductoBase):
    pass

class Producto(ProductoBase):
    id: int

    class Config:
        orm_mode = True


