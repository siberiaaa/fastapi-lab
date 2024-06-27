from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine #!aaaaaaa
import metodos_envios.models as models 
import metodos_envios.schemas as schemas
import metodos_envios.service as service

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('', response_model=list[schemas.Metodo_Envio])
def listar_metodos_envios(db: Session = Depends(get_db)):
    return service.listar_metodos_envios(db=db)

@router.post('', response_model=schemas.Metodo_Envio)
def crear_metodo_envio(metodo_envio: schemas.Metodo_EnvioCrear, db: Session = Depends(get_db)):
    return service.crear_metodo_envio(db=db, metodo_envio=metodo_envio)
