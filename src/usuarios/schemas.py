from pydantic import BaseModel, field_validator
from typing import Union
from datetime import datetime
from email_validator import validate_email, EmailNotValidError

class UsuarioBase(BaseModel):
    cedula: str
    nombres: str
    apellidos: str
    nacimiento: datetime
    direccion: str
    correo: str
    contraseña: str
    tipo_id: int

    @field_validator('correo')
    def validacion(cls, correo): 
        try: 
            validado = validate_email(correo)
            correo = validado.email
            return correo
        except EmailNotValidError as e: 
            raise ValueError('El email no es válido')


class UsuarioCrear(UsuarioBase):
    pass

class Usuario(UsuarioBase):

    class Config:
        orm_mode = True


