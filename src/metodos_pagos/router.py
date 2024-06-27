from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine #!aaaaaaa
import metodos_pagos.models as models 
import metodos_pagos.schemas as schemas
import metodos_pagos.service as service

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('', response_model=list[schemas.Metodo_Pago])
def home(db: Session = Depends(get_db)):
    return service.listar_metodos_pagos(db=db)

@router.post('', response_model=schemas.Metodo_Pago)
def crear_metodo_pago(metodo_pago: schemas.Metodo_PagoCrear, db: Session = Depends(get_db)):
    return service.crear_metodo_pago(db=db, metodo_pago=metodo_pago)

