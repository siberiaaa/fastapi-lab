from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine #!aaaaaaa
import estados_compras.models as models 
import estados_compras.schemas as schemas
import estados_compras.service as service

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('', response_model=list[schemas.Estado_Compra])
def listar_estados_compras(db: Session = Depends(get_db)):
    return service.listar_estado_compra(db=db)

@router.post('', response_model=schemas.Estado_Compra)
def crear_estado_compra(estado_compra: schemas.Estado_CompraCrear, db: Session = Depends(get_db)):
    return service.crear_estado_compra(db=db, estado_compra=estado_compra)



