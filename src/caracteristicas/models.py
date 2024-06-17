from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base #!aaaaaaa

class Caracteristica(Base): 
    __tablename__  = "caracteristicas"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String, index=True)
    explicacion = Column(String, index=True)
    encargo_id = Column(Integer, ForeignKey('compras.id'))
    estado_caracteristica_id = Column(Integer, ForeignKey('estados_caracteristicas.id'))

    encargo = relationship('Compra', back_populates='caracteristicas')
    estado_caracteristica = relationship('Estado_Caracteristica', back_populates='caracteristicas')