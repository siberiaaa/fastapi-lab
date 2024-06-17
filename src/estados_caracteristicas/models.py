from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base #!aaaaaaa

class Estado_Caracteristica(Base): 
    __tablename__  = "estados_caracteristicas"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String, index=True)
    descripcion = Column(String, index=True)

    caracteristicas = relationship('Caracteristica', back_populates='estado_caracteristica')