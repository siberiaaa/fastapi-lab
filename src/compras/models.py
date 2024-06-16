from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base #!aaaaaaa

class Compra(Base): 
    __tablename__  = "compras"
    
    id = Column(Integer, primary_key=True)
    cantidad = Column(Integer, index=True)
    fecha = Column(DateTime, index=True)
    cliente_cedula = Column(String, ForeignKey('usuarios.cedula'))
    producto_id = Column(Integer, ForeignKey('productos.id'))
    tipo_compra_id = Column(Integer, ForeignKey('tipos_compras.id'))
    estado_compra_id = Column(Integer, ForeignKey('estados_compras.id'))

    cliente = relationship('Usuario', back_populates='compras')
    producto = relationship('Producto', back_populates='compras')
    tipo_compra = relationship('Tipo_Compra', back_populates='compras')
    estado_compra = relationship('Estado_Compra', back_populates='compras')