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

@router.get('', response_model=list[schemas.Estado_Caracteristica])
def listar_estados_caracteristicas(db : Session = Depends(get_db)):
    estados_carateristicas = service.listar_estados_caracteristicas(db=db)
    return estados_carateristicas

@router.post('', response_model=schemas.Estado_Caracteristica)
def crear_estado_caracteristica(estado_caracteristica: schemas.Estado_CaracteristicaCrear, db: Session = Depends(get_db)):
    return service.crear_estado_caracteristica(db=db, estado_caracteristica=estado_caracteristica)

@router.get('/{id}', response_model=schemas.Estado_Caracteristica)
def buscar_estado_caracteristica(id : int, db : Session = Depends(get_db)): 
    return