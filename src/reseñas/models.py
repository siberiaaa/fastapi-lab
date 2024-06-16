from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base #!aaaaaaa

class Reseña(Base): 
    __tablename__  = "reseñas"
    
    id = Column(Integer, primary_key=True)
    invencion = Column(DateTime, index=True)
    inventor = Column(String, index=True)
    años_produccion = Column(Integer, index=True)
    producto_id = Column(Integer, ForeignKey('productos.id'))

    producto = relationship('Producto', back_populates='reseñas')