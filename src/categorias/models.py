from sqlalchemy import Column, Integer, String
from database import Base #!aaaaaaa

class Categoria(Base):
    __tablename__  = "categorias"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String, index=True)
    descripcion = Column(String, index=True)


class Tipo_Usuario(Base): 
    __tablename__  = "tipos_usuarios"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String, index=True)
    descripcion = Column(String, index=True)

class Tipo_Compra(Base): 
    __tablename__  = "tipos_compras"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String, index=True)
    descripcion = Column(String, index=True)

class Estado_Cotizacion(Base): 
    __tablename__  = "estados_cotizacion"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String, index=True)
    descripcion = Column(String, index=True)

class Metodo_Pago(Base): 
    __tablename__  = "metodos_pagos"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String, index=True)
    descripcion = Column(String, index=True)

class Metodo_Envio(Base): 
    __tablename__  = "metodos_envios"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String, index=True)
    descripcion = Column(String, index=True)

class Estado_Caracteristica(Base): 
    __tablename__  = "estados_caracteristicas"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String, index=True)
    descripcion = Column(String, index=True)

class Estado_Compra(Base): 
    __tablename__  = "estados_compras"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String, index=True)
    descripcion = Column(String, index=True)

