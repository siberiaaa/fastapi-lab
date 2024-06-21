from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from schemas import Respuesta
import tipos_producto.models as models 
import tipos_producto.schemas as schemas
import tipos_producto.service as service

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

@router.get('', response_model=Respuesta[list[schemas.Tipo_Producto]])
def get_tipos_productos(db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)):
    return service.get_tipos_producto(db=db)

@router.post('', response_model=Respuesta[schemas.Tipo_Producto])
def crear_tipo_producto(tipo_producto: schemas.Tipo_ProductoCrear, db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)):
    return service.create_tipo_producto(db=db, tipo_producto=tipo_producto)

@router.get('/{id}', response_model=Respuesta[schemas.Tipo_Producto])
def get_tipo_producto(id: int, db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)): 
    return service.get_tipo_producto(db=db, id=id)

@router.put('/{id}', response_model=Respuesta[schemas.Tipo_Producto])
def update_tipo_producto(id: int, tipo_producto: schemas.Tipo_ProductoCrear, db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)): 
    return service.update_tipo_producto(db=db, id=id, tipo_producto=tipo_producto)

@router.delete('/{id}', response_model=Respuesta[schemas.Tipo_Producto])
def eliminar_tipo_producto(id: int, db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)): 
    return service.delete_tipo_producto(db=db, id=id)