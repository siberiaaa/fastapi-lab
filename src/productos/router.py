from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine #!aaaaaaa
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

@router.get('', response_model=list[schemas.Producto])
def listar_productos(db: Session = Depends(get_db)):
    return service.listar_tipos_productos(db=db)

@router.post('', response_model=schemas.Producto)
def crear_producto(producto: schemas.ProductoCrear, db: Session = Depends(get_db)):
    return service.crear_producto(db=db, producto=producto)

@router.get('/{id}', response_model=schemas.Producto)
def buscar_producto(id : int, db: Session = Depends(get_db)): 
    return service.buscar_producto(db=db, id=id)

@router.put('/{id}', response_model=schemas.Producto)
def modificar_producto(id : int, producto: schemas.ProductoCrear, db: Session = Depends(get_db)): 
    return service.modificar_producto(db=db, id=id, producto=producto)

@router.delete('/{id}', response_model=schemas.Producto)
def eliminar_producto(id : int, db: Session = Depends(get_db)): 
    return service.eliminar_producto(db=db, id=id)