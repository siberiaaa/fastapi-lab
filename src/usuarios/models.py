from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base #!aaaaaaa

# class Usuario(Base): 
#     __tablename__  = "usuarios"
    
#     cedula = Column(String, primary_key=True)
#     nombres = Column(String, index=True)
#     apellidos = Column(String, index=True)
#     nacimiento = Column(DateTime, index=True)
#     direccion = Column(String, index=True)
#     correo = Column(String, index=True)
#     contraseña = Column(String, index=True)
#     tipo_id = Column(Integer, ForeignKey("tipos_usuarios.id"))

#     tipo = relationship(back_populates='usuarios')