from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine #!aaaaaaa
import tipos_usuario.models as models 
import tipos_usuario.schemas as schemas
import tipos_usuario.service as service

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('')
def home():
    return {"message":"Hello world desde el router opa"}

@router.post('', response_model=schemas.Tipo_Usuario)
def crear_categoria(tipo_usuario: schemas.Tipo_UsuarioCrear, db: Session = Depends(get_db)):
    return service.crear_tipo_usuario(db=db, tipo_usuario=tipo_usuario)

