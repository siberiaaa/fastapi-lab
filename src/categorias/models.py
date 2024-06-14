from sqlalchemy import Column, Integer, String
from database import Base #!aaaaaaa

class Categoria(Base):
    __tablename__  = "categorias"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String, index=True)
    descripcion = Column(String, index=True)

