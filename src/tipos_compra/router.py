from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine #!aaaaaaa
import tipos_compra.models as models 
import tipos_compra.schemas as schemas
import tipos_compra.service as service

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('', response_model=list[schemas.Tipo_Compra])
def listar_tipos_compras(db: Session = Depends(get_db)):
    return service.listar_tipos_compras(db=db)

@router.post('', response_model=schemas.Tipo_Compra)
def crear_tipo_compra(tipo_compra: schemas.Tipo_CompraCrear, db: Session = Depends(get_db)):
    return service.crear_tipo_compra(db=db, tipo_compra=tipo_compra)

