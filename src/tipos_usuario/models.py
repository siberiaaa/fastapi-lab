from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base #!aaaaaaa

class Tipo_Usuario(Base): 
    __tablename__  = "tipos_usuarios"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String, index=True)
    descripcion = Column(String, index=True)

    usuarios = relationship("Usuario", back_populates='tipo')