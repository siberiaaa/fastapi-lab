from fastapi import APIRouter, Depends, Form, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from schemas import Respuesta
#from usuarios.router import oauth2_scheme
from typing import Annotated
from database import SessionLocal, engine #!aaaaaaa
import calificaciones.models as models 
import calificaciones.schemas as schemas
import calificaciones.service as service

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

@router.get('', response_model=list[schemas.Calificacion])
def listar_calificaciones(db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)):
    return service.listar_calificaciones(db=db)

@router.get('/producto/{id}', response_model=list[schemas.Calificacion])
def listar_calificaciones_producto(id: int,  db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)):
    return service.listar_calificaciones_productos(db=db, id=id)

@router.get('/cliente/{cedula}', response_model=list[schemas.Calificacion])
def listar_calificaciones_cliente(cedula: str,  db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)):
    return service.listar_calificaciones_clientes(db=db, cedula=cedula)

@router.post('')
def crear_calificacion(titulo: str = Form(...), 
                       comentario: str = Form(...), 
                       estrellas: str = Form(...), 
                       emoticono: str = Form(...), 
                       producto: int = Form(...), 
                       db: Session = Depends(get_db), 
                       info=Depends(auth_handler.auth_wrapper)):
    calificacion = schemas.CalificacionCrear(
        titulo=titulo, comentario=comentario, 
        estrellas=estrellas, emoticono=emoticono, 
        usuario_cedula=info['cedula'], producto_id=producto
    )
    
    service.crear_calificacion(db=db, calificacion=calificacion)
    return RedirectResponse(url=f'/productos/{producto}', status_code=status.HTTP_303_SEE_OTHER)

@router.get('/{id}', response_model=schemas.Calificacion)
def buscar_calificacion(id : int,  db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)): 
    return service.buscar_calificacion(db=db, id=id)

@router.put('/{id}', response_model=schemas.Calificacion)
def modificar_calificacion(id : int, calificacion: schemas.CalificacionCrear, db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)): 
    return service.modificar_calificacion(db=db, id=id, calificacion=calificacion)

@router.delete('/{id}', response_model=schemas.Calificacion)
def eliminar_calificacion(id : int,  db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)): 
    return service.eliminar_calificacion(db=db, id=id)