from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine #!aaaaaaa
import caracteristicas.models as models 
import caracteristicas.schemas as schemas
import caracteristicas.service as service

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('', response_model=list[schemas.Caracteristica])
def listar_caracteristicas(db: Session = Depends(get_db)):
    return service.listar_caracteristicas(db=db)

@router.post('', response_model=schemas.Caracteristica)
def crear_caracteristica(caracteristica: schemas.CaracteristicaCrear, db: Session = Depends(get_db)):
    return service.crear_caracteristica(db=db, caracteristica=caracteristica)

@router.get('/{id}', response_model=schemas.Caracteristica)
def buscar_caracteristica(id : int, db: Session = Depends(get_db)): 
    return service.buscar_caracteristica(db=db, id=id)

@router.put('/{id}', response_model=schemas.Caracteristica)
def modificar_caracteristica(id : int, caracteristica: schemas.CaracteristicaCrear, db: Session = Depends(get_db)): 
    return service.modificar_caracteristica(db=db, id=id, caracteristica=caracteristica)

@router.delete('/{id}', response_model=schemas.Caracteristica)
def eliminar_caracteristica(id : int, db: Session = Depends(get_db)): 
    return service.eliminar_caracteristica(db=db, id=id)