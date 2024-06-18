from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine #!aaaaaaa
import usuarios.models as models 
import usuarios.schemas as schemas
import usuarios.service as service

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('/registrar', response_model=schemas.Usuario)
def registrar_usuario(usuario: schemas.UsuarioCrear, db: Session = Depends(get_db)):
    return service.crear_usuario(db=db, usuario=usuario)

@router.post('/iniciar_sesion', response_model=schemas.Usuario)
def iniciar_sesion(): 
    return 'holaaaaaaaa'