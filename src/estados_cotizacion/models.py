from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Estado_Cotizacion(Base): 
    __tablename__  = "estados_cotizacion"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String, index=True)
    descripcion = Column(String, index=True)

    cotizaciones = relationship('Cotizacion', back_populates='estado_cotizacion')