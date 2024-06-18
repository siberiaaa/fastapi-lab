from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from sqlalchemy.orm import Session
from database import SessionLocal, engine #!aaaaaaa
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from schemas import Token, Respuesta
import usuarios.models as models 
import usuarios.schemas as schemas
import usuarios.service as service

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 15

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="iniciar_sesion")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('/registrar', response_model=Respuesta[schemas.Usuario])
def registrar_usuario(usuario: schemas.UsuarioCrear, db: Session = Depends(get_db)):
    return service.registrar_usuario(db=db, usuario=usuario)

@router.delete('/usuario/{cedula}', response_model=schemas.Usuario)
def borrar_usuario(cedula : str, db: Session = Depends(get_db)): 
    return service.eliminar_usuario(db=db, cedula=cedula)

@router.post('/iniciar_sesion', response_model=Token)
def iniciar_sesion(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]): 
    usuario = service.autenticar_usuario(form_data.username, form_data.password)
    if usuario == False: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Credenciales incorrectas', 
            headers={"WWW-Authenticate": "Bearer"}
        )
    tiempo_expiracion = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_acceso = service.crear_token_acceso(
        data={'cedula': usuario.cedula}, 
        expires_delta=tiempo_expiracion
    )
    return Token(usuario=f'{usuario.nombres} {usuario.apellidos}', token_acceso=token_acceso, tipo_token='bearer')