from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine #!aaaaaaa
import facturas.models as models 
import facturas.schemas as schemas
import facturas.service as service

from usuarios.service import AuthHandler
auth_handler = AuthHandler()

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('', response_model=list[schemas.Factura])
def listar_facturas(db: Session = Depends(get_db)):
    return service.listar_facturas(db=db)

@router.post('', response_model=schemas.Factura)
def crear_factura(factura: schemas.FacturaCrear, db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)):
    return service.crear_factura(db=db, factura=factura)

@router.get('/{id}', response_model=schemas.Factura)
def buscar_factura(id : int, db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)): 
    return service.buscar_factura(db=db, id=id)

# @router.put('/{id}', response_model=schemas.Factura)
# def modificar_factura(id : int, factura: schemas.FacturaCrear, db: Session = Depends(get_db)): 
#     return service.modificar_factura(db=db, id=id, factura=factura)

# @router.delete('/{id}', response_model=schemas.Factura)
# def eliminar_factura(id : int, db: Session = Depends(get_db)): 
#     return service.eliminar_factura(db=db, id=id)