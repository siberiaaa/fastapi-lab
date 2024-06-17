from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base #!aaaaaaa

class Metodo_Envio(Base): 
    __tablename__  = "metodos_envios"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String, index=True)
    descripcion = Column(String, index=True)

    facturas = relationship('Factura', back_populates='metodo_envio')