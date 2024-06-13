from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine #!aaaaaaa
import categorias.models as models
import categorias.schemas as schemas
import categorias.service as service

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

@router.post('', response_model=schemas.Categoria)
def crear_categoria(categoria: schemas.CategoriaCrear, db: Session = Depends(get_db)):
    return service.crear_categoria(db=db, categoria=categoria)



