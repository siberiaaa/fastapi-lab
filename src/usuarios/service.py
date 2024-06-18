from sqlalchemy.orm import Session
from typing import Union
from datetime import timedelta, datetime, timezone
from jose import jwt
from schemas import Respuesta, Token
import usuarios.models as models
import usuarios.schemas as schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "27A0D7C4CCCE76E6BE39225B7EEE8BD0EF890DE82D49E459F4C405C583080AB0"
ALGORITHM = "HS256"

def registrar_usuario(db: Session, usuario: schemas.UsuarioCrear):
    db_usuario = models.Usuario(
        cedula=usuario.cedula, 
        nombres=usuario.nombres, 
        apellidos=usuario.apellidos, 
        direccion=usuario.direccion, 
        nacimiento=usuario.nacimiento, 
        correo=usuario.correo, 
        contraseña=obtener_hash(usuario.contraseña), 
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
        contraseña=usuario.contraseña, 
        tipo_id=db_usuario.tipo_id
    )
    respuesta = Respuesta[schemas.Usuario](
        ok = True, 
        mensaje = 'Usuario registrado exitósamente. ADVERTENCIA: ESTA ES LA ÚLTIMA VEZ QUE VERÁ SU CONTRASEÑA LIBREMENTE', 
        data = actual
    )
    return respuesta

def eliminar_usuario(db: Session, cedula: str): 
    usuario = db.query(models.Usuario).filter(models.Usuario.cedula == cedula).first()
    db.delete(usuario)
    db.commit()
    return usuario

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

def autenticar_usuario(db: Session, cedula: str, contraseña: str):
    usuario = obtener_usuario(db, cedula)
    print('Obtenido')
    print(usuario)
    if not usuario:
        return False
    # contraseña_hasheada = obtener_hash(usuario.contraseña_hasheada)
    if not verificar_contraseña(contraseña, usuario.contraseña):
        return False
    return usuario

def crear_token_acceso(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt