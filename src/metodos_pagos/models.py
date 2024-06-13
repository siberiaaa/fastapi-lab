from sqlalchemy import Column, Integer, String
from database import Base #!aaaaaaa

class Metodo_Pago(Base): 
    __tablename__  = "metodos_pagos"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String, index=True)
    descripcion = Column(String, index=True)
