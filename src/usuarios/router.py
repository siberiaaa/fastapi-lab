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

@router.get('', response_model=list[schemas.Usuario])
def listar_usuarios(db: Session = Depends(get_db)):
    return service.listar_tipos_usuarios(db=db)

@router.post('', response_model=schemas.Usuario)
def crear_usuario(usuario: schemas.UsuarioCrear, db: Session = Depends(get_db)):
    return service.crear_usuario(db=db, usuario=usuario)

@router.get('/{id}', response_model=schemas.Usuario)
def buscar_usuario(id : int, db: Session = Depends(get_db)): 
    return service.buscar_usuario(db=db, id=id)