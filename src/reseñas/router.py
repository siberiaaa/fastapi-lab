from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine #!aaaaaaa
import reseñas.models as models 
import reseñas.schemas as schemas
import reseñas.service as service

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('', response_model=list[schemas.Reseña])
def listar_reseñas(db: Session = Depends(get_db)):
    return service.listar_tipos_reseñas(db=db)

@router.post('', response_model=schemas.Reseña)
def crear_reseña(reseña: schemas.ReseñaCrear, db: Session = Depends(get_db)):
    return service.crear_reseña(db=db, reseña=reseña)

@router.get('/{id}', response_model=schemas.Reseña)
def buscar_reseña(id : int, db: Session = Depends(get_db)): 
    return service.buscar_reseña(db=db, id=id)

@router.put('/{id}', response_model=schemas.Reseña)
def modificar_reseña(id : int, reseña: schemas.ReseñaCrear, db: Session = Depends(get_db)): 
    return service.modificar_reseña(db=db, id=id, reseña=reseña)

@router.delete('/{id}', response_model=schemas.Reseña)
def eliminar_reseña(id : int, db: Session = Depends(get_db)): 
    return service.eliminar_reseña(db=db, id=id)