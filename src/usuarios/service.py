from sqlalchemy.orm import Session
from schemas import Respuesta
import usuarios.models as models
import usuarios.schemas as schemas

def registrar_usuario(db: Session, usuario: schemas.UsuarioCrear):
    db_usuario = models.Usuario(
        cedula=usuario.cedula, 
        nombres=usuario.nombres, 
        apellidos=usuario.apellidos, 
        direccion=usuario.direccion, 
        nacimiento=usuario.nacimiento, 
        correo=usuario.correo, 
        contraseña=usuario.contraseña, 
        tipo_id=usuario.tipo_id)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def listar_usuarios(db: Session): 
    return db.query(models.Usuario).all()

def buscar_usuario(db: Session, cedula: str): 
    returned = db.query(models.Usuario).filter(models.Usuario.cedula == cedula).first()

    if returned == None:
        return Respuesta[schemas.Categoria](ok=False, mensaje='Usuario no encontrado')

    usuario = schemas.Usuario(cedula=returned.cedula, 
        nombres=returned.nombres, 
        apellidos=returned.apellidos, 
        direccion=returned.direccion, 
        nacimiento=returned.nacimiento, 
        correo=returned.correo, 
        contraseña=returned.contraseña, 
        tipo_id=returned.tipo_id) 
    
    return Respuesta[schemas.Categoria](ok=True, mensaje='Usuario encontrado', data=usuario)

