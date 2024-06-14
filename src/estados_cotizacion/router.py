from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine #!aaaaaaa
import estados_cotizacion.models as models 
import estados_cotizacion.schemas as schemas
import estados_cotizacion.service as service

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

@router.post('', response_model=schemas.Estado_Cotizacion)
def crear_categoria(estado_cotizacion: schemas.Estado_CotizacionCrear, db: Session = Depends(get_db)):
    return service.crear_estado_cotizacion(db=db, estado_cotizacion=estado_cotizacion)


