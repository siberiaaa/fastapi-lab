from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base #!aaaaaaa

class Anecdota(Base): 
    __tablename__  = "anecdotas"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String, index=True)
    descripcion = Column(String, index=True)
    reseña_id = Column(Integer, ForeignKey('reseñas.id'))

    reseña = relationship('Reseña', back_populates='anecdotas')