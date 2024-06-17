from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base #!aaaaaaa

class Cotizacion(Base): 
    __tablename__  = "cotizaciones"
    
    id = Column(Integer, primary_key=True)
    precio = Column(Float, index=True)
    compra_id = Column(Integer, ForeignKey('compras.id'))
    estado_cotizacion_id = Column(Integer, ForeignKey('estados_compras.id'))

    compra = relationship('Compra', back_populates='cotizaciones')
    estado_cotizacion = relationship('Estado_Cotizacion', back_populates='cotizaciones')
    factura = relationship('Factura', back_populates='cotizacion')