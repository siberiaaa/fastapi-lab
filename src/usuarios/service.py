from sqlalchemy.orm import Session
from schemas import Respuesta, Token
import usuarios.models as models
import usuarios.schemas as schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
    actual = schemas.Usuario(
        cedula=db_usuario.cedula, 
        nombres=db_usuario.nombres, 
        apellidos=db_usuario.apellidos, 
        direccion=db_usuario.direccion, 
        nacimiento=db_usuario.nacimiento, 
        correo=db_usuario.correo, 
        contraseña=db_usuario.contraseña, 
        tipo_id=db_usuario.tipo_id
    )
    respuesta = Respuesta[schemas.Usuario](
        ok = True, 
        mensaje = 'Usuario registrado exitósamente', 
        data = actual
    )
    return respuesta

def listar_usuarios(db: Session): 
    return db.query(models.Usuario).all()

def buscar_usuario(db: Session, cedula: str): 
    retornado = db.query(models.Usuario).filter(models.Usuario.cedula == cedula).first()

    if retornado == None:
        return Respuesta[schemas.Usuario](ok=False, mensaje='Usuario no encontrado')

    usuario = schemas.Usuario(
        cedula=retornado.cedula, 
        nombres=retornado.nombres, 
        apellidos=retornado.apellidos, 
        direccion=retornado.direccion, 
        nacimiento=retornado.nacimiento, 
        correo=retornado.correo, 
        contraseña=retornado.contraseña, 
        tipo_id=retornado.tipo_id) 
    
    return Respuesta[schemas.Usuario](ok=True, mensaje='Usuario encontrado', data=usuario)


def obtener_usuario(db: Session, cedula: str):
    return db.query(models.Usuario).filter(models.Usuario.cedula == cedula).first()

def obtener_hash(contraseña):
    return pwd_context.hash(contraseña)

def verificar_contraseña(contraseña_simple, contraseña_hasheada):
    return pwd_context.verify(contraseña_simple, contraseña_hasheada)

def autenticar_usuario(cedula: str, contraseña: str):
    usuario = obtener_usuario(cedula)
    print('Obtenido')
    print(usuario)
    if not usuario:
        return False
    # contraseña_hasheada = obtener_hash(usuario.contraseña_hasheada)
    if not verificar_contraseña(contraseña, usuario.contraseña):
        return False
    return usuario