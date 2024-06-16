from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from database import Base #!aaaaaaa

class Tipo_Producto(Base): 
    __tablename__  = "tipos_productos"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String, index=True)
    descripcion = Column(String, index=True)
    funcionalidad = Column(Boolean, index=True)

    productos = relationship('Producto', back_populates='tipo_producto')