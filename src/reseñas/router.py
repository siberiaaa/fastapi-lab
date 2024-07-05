from fastapi import APIRouter, Depends, Form, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import Annotated
from database import SessionLocal, engine
from datetime import datetime
import reseñas.models as models 
import reseñas.schemas as schemas
import reseñas.service as service
#from usuarios.router import oauth2_scheme noono

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

from usuarios.service import AuthHandler
auth_handler = AuthHandler()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('', response_model=list[schemas.Reseña])
def listar_reseñas(db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)):
    return service.listar_reseñas(db=db)

@router.get('/producto/{id}', response_model=list[schemas.Reseña])
def listar_reseñas(id: int, db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)):
    return service.listar_reseñas_productos(db=db, id=id)

@router.post('')
def crear_reseña(invencion: datetime = Form(...), 
                 inventor: str = Form(...), 
                 años_produccion: float = Form(...), 
                 producto_real: int = Form(...), 
                 db: Session = Depends(get_db), 
                 info=Depends(auth_handler.auth_wrapper)): 
    print(invencion)
    reseña = schemas.ReseñaCrear(
        invencion=invencion, 
        inventor=inventor, 
        años_produccion=años_produccion, 
        producto_id=producto_real
    )
    service.crear_reseña(db=db, reseña=reseña)
    return RedirectResponse(url=f'/productos/{producto_real}', status_code=status.HTTP_303_SEE_OTHER)

@router.get('/{id}', response_model=schemas.Reseña)
def buscar_reseña(id : int, db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)): 
    return service.buscar_reseña(db=db, id=id)

@router.put('/{id}', response_model=schemas.Reseña)
def modificar_reseña(id : int, reseña: schemas.ReseñaCrear, db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)): 
    return service.modificar_reseña(db=db, id=id, reseña=reseña)

@router.delete('/{id}', response_model=schemas.Reseña)
def eliminar_reseña(id : int, db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)): 
    return service.eliminar_reseña(db=db, id=id)