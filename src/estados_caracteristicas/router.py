from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine #!aaaaaaa
import estados_caracteristicas.models as models 
import estados_caracteristicas.schemas as schemas
import estados_caracteristicas.service as service

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

@router.post('', response_model=schemas.Estado_Caracteristica)
def crear_categoria(estado_caracteristica: schemas.Estado_CaracteristicaCrear, db: Session = Depends(get_db)):
    return service.crear_estado_caracteristica(db=db, estado_caracteristica=estado_caracteristica)


