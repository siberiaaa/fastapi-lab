from sqlalchemy.orm import Session
from typing import Union, Any
from datetime import timedelta, datetime, timezone
from jose import jwt
from schemas import Respuesta, Token
from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import usuarios.models as models
import usuarios.schemas as schemas
from passlib.context import CryptContext

class AuthHandler():
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = "27A0D7C4CCCE76E6BE39225B7EEE8BD0EF890DE82D49E459F4C405C583080AB0"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 5

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=self.ALGORITHM)
            return payload
        except jwt.ExpiredSignatureError:
            raise RequiresLoginException()
        except jwt.JWTError as e:
            raise RequiresLoginException()
        # except Exception as e:
        #     raise RequiresLoginException()
        #!comentado esto de arriba para no morir en el intento de debbugear
            
    
    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)


    def create_access_token(self, data: dict, expires_delta: timedelta = None) -> str:
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes= self.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode = data.copy()
        to_encode.update({"exp": expire})
        #to_encode = {"exp": expire, "sub": str(subject)} Si no funciona lo de arriba toca esto
        
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def get_hash_password(self, plain_password):
        return self.pwd_context.hash(plain_password)


    def verify_password(self, plain_password, hash_password):
        return self.pwd_context.verify(plain_password, hash_password)


    async def authenticate_user(self, db: Session, cedula: str, contraseña: str):
        try:
            usuario = obtener_usuario(db, cedula)
            if usuario: 
                password_check = self.verify_password(contraseña, usuario.contraseña)
                if password_check: 
                    return usuario
                else: 
                    return False
                #return password_check #Nuestro código original retornaba el usuario (?)
                #por una buena razon lo retornaba
            else: 
                return False
        except:
            raise RequiresLoginException()

    def registrar_usuario(self, db: Session, usuario: schemas.UsuarioCrear):
        db_usuario = models.Usuario(
            cedula=usuario.cedula, 
            nombres=usuario.nombres, 
            apellidos=usuario.apellidos, 
            direccion=usuario.direccion, 
            nacimiento=usuario.nacimiento, 
            correo=usuario.correo, 
            contraseña=self.get_hash_password(usuario.contraseña), 
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


class RequiresLoginException(Exception):
    pass





#Métodos principalmente para interactuar con la base de datos que por ahora no pondremos en la clase de arriba
def eliminar_usuario(db: Session, cedula: str): 
    usuario = db.query(models.Usuario).filter(models.Usuario.cedula == cedula).first()
    db.delete(usuario)
    db.commit()
    return usuario

def listar_usuarios(db: Session): 
    return db.query(models.Usuario).all()

def listar_artesanos(db: Session): 
    return db.query(models.Usuario).filter(models.Usuario.tipo_id == 1).all()

def listar_clientes(db: Session): 
    return db.query(models.Usuario).filter(models.Usuario.tipo_id == 2).all()

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




