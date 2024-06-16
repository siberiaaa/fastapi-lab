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


@router.post('', response_model=schemas.Usuario)
def crear_usuario(usuario: schemas.UsuarioCrear, db: Session = Depends(get_db)):
    return service.crear_usuario(db=db, usuario=usuario)
