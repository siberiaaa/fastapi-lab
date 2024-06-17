from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine #!aaaaaaa
import cotizaciones.models as models 
import cotizaciones.schemas as schemas
import cotizaciones.service as service

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('', response_model=list[schemas.Cotizacion])
def listar_cotizaciones(db: Session = Depends(get_db)):
    return service.listar_cotizaciones(db=db)

@router.post('', response_model=schemas.Cotizacion)
def crear_cotizacion(cotizacion: schemas.CotizacionCrear, db: Session = Depends(get_db)):
    return service.crear_cotizacion(db=db, cotizacion=cotizacion)

@router.get('/{id}', response_model=schemas.Cotizacion)
def buscar_cotizacion(id : int, db: Session = Depends(get_db)): 
    return service.buscar_cotizacion(db=db, id=id)

@router.put('/{id}', response_model=schemas.Cotizacion)
def modificar_cotizacion(id : int, cotizacion: schemas.CotizacionCrear, db: Session = Depends(get_db)): 
    return service.modificar_cotizacion(db=db, id=id, cotizacion=cotizacion)

@router.delete('/{id}', response_model=schemas.Cotizacion)
def eliminar_cotizacion(id : int, db: Session = Depends(get_db)): 
    return service.eliminar_cotizacion(db=db, id=id)