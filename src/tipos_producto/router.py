from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine #!aaaaaaa
import tipos_producto.models as models 
import tipos_producto.schemas as schemas
import tipos_producto.service as service

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('', response_model=list[schemas.Tipo_Producto])
def listar_tipos_productos(db: Session = Depends(get_db)):
    return service.listar_tipos_productos(db=db)

@router.post('', response_model=schemas.Tipo_Producto)
def crear_tipo_producto(tipo_producto: schemas.Tipo_ProductoCrear, db: Session = Depends(get_db)):
    return service.crear_tipo_producto(db=db, tipo_producto=tipo_producto)

@router.get('/{id}', response_model=schemas.Tipo_Producto)
def buscar_tipo_producto(id : int, db: Session = Depends(get_db)): 
    return service.buscar_tipo_producto(db=db, id=id)

@router.put('/{id}', response_model=schemas.Tipo_Producto)
def modificar_tipo_producto(id : int, tipo_producto: schemas.Tipo_ProductoCrear, db: Session = Depends(get_db)): 
    return service.modificar_tipo_producto(db=db, id=id, tipo_producto=tipo_producto)

@router.delete('/{id}', response_model=schemas.Tipo_Producto)
def eliminar_tipo_producto(id : int, db: Session = Depends(get_db)): 
    return service.eliminar_tipo_producto(db=db, id=id)