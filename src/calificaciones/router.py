from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine #!aaaaaaa
import calificaciones.models as models 
import calificaciones.schemas as schemas
import calificaciones.service as service

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('', response_model=list[schemas.Calificacion])
def listar_calificaciones(db: Session = Depends(get_db)):
    return service.listar_calificaciones(db=db)

@router.post('', response_model=schemas.Calificacion)
def crear_calificacion(calificacion: schemas.CalificacionCrear, db: Session = Depends(get_db)):
    return service.crear_calificacion(db=db, calificacion=calificacion)

@router.get('/{id}', response_model=schemas.Calificacion)
def buscar_calificacion(id : int, db: Session = Depends(get_db)): 
    return service.buscar_calificacion(db=db, id=id)

@router.put('/{id}', response_model=schemas.Calificacion)
def modificar_calificacion(id : int, calificacion: schemas.CalificacionCrear, db: Session = Depends(get_db)): 
    return service.modificar_calificacion(db=db, id=id, calificacion=calificacion)

@router.delete('/{id}', response_model=schemas.Calificacion)
def eliminar_calificacion(id : int, db: Session = Depends(get_db)): 
    return service.eliminar_calificacion(db=db, id=id)