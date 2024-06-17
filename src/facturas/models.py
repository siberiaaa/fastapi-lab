from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base #!aaaaaaa

class Factura(Base): 
    __tablename__  = "facturas"
    
    id = Column(Integer, primary_key=True)
    fecha_entrega = Column(DateTime, index=True)
    cotizacion_id = Column(Integer, ForeignKey('cotizaciones.id'))
    metodo_pago_id = Column(Integer, ForeignKey('metodos_pagos.id'))
    metodo_envio_id = Column(Integer, ForeignKey('metodos_envios.id'))

    cotizacion = relationship('Cotizacion', back_populates='factura')
    metodo_pago = relationship('Metodo_Pago', back_populates='facturas')
    metodo_envio = relationship('Metodo_Envio', back_populates='facturas')