from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from schemas import Respuesta
import productos.models as models 
import productos.schemas as schemas
import productos.service as service

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('', response_model=Respuesta[list[schemas.Producto]])
def get_productos(db: Session = Depends(get_db)):
    return service.get_productos(db=db)

@router.post('', response_model=Respuesta[schemas.Producto])
def create_producto(producto: schemas.ProductoCrear, db: Session = Depends(get_db)):
    return service.create_producto(db=db, producto=producto)

@router.get('/{id}', response_model=Respuesta[schemas.Producto])
def get_producto(id : int, db: Session = Depends(get_db)): 
    return service.get_producto(db=db, id=id)

@router.get('/artesano/{cedula_artesano}', response_model=Respuesta[list[schemas.Producto]])
def get_productos_artesano(cedula_artesano : int, db: Session = Depends(get_db)): 
    return service.get_productos_por_artesano(db=db, cedula_artesano=cedula_artesano)

@router.put('/{id}', response_model=Respuesta[schemas.Producto])
def update_producto(id : int, producto: schemas.ProductoCrear, db: Session = Depends(get_db)): 
    return service.update_producto(db=db, id=id, producto=producto)

@router.delete('/{id}', response_model=Respuesta[schemas.Producto])
def delete_producto(id : int, db: Session = Depends(get_db)): 
    return service.delete_producto(db=db, id=id)