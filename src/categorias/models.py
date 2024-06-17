from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Categoria(Base):
    __tablename__  = "categorias"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String, index=True)
    descripcion = Column(String, index=True)

    productos = relationship('Producto', back_populates='categoria')