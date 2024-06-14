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

@router.get('')
def home():
    return {"message":"Hello world desde el router opa"}

@router.post('', response_model=schemas.Estado_Compra)
def crear_categoria(estado_compra: schemas.Estado_CompraCrear, db: Session = Depends(get_db)):
    return service.crear_estado_compra(db=db, estado_compra=estado_compra)



