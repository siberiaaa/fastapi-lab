from sqlalchemy import Column, Integer, String
from database import Base #!aaaaaaa

class Tipo_Compra(Base): 
    __tablename__  = "tipos_compras"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String, index=True)
    descripcion = Column(String, index=True)