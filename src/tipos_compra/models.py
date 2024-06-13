from sqlalchemy import Column, Integer, String
from database import Base #!aaaaaaa

class Tipo_Compra(Base): 
    __tablename__  = "tipos_compras"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String, index=True)
    descripcion = Column(String, index=True)

class Tipo_Usuario(Base): 
    __tablename__  = "tipos_usuarios"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String, index=True)
    descripcion = Column(String, index=True)

class Tipo_Producto(Base): 
    __tablename__  = "tipos_productos"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String, index=True)
    descripcion = Column(String, index=True)

