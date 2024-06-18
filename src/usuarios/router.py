from fastapi import APIRouter, Depends
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

SECRET_KEY = "27A0D7C4CCCE76E6BE39225B7EEE8BD0EF890DE82D49E459F4C405C583080AB0"
ALGORITHM = "HS256"
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

@router.post('/iniciar_sesion', response_model=schemas.Usuario)
def iniciar_sesion(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]): 
    return 'holaaaaaaaa'