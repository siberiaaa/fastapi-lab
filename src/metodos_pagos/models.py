from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Metodo_Pago(Base): 
    __tablename__  = "metodos_pagos"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String, index=True)
    descripcion = Column(String, index=True)

    facturas = relationship('Factura', back_populates='metodo_pago')