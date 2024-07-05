from fastapi import APIRouter, Depends, Form ,status
from fastapi.responses import RedirectResponse
from typing import Annotated
from sqlalchemy.orm import Session
from database import SessionLocal, engine
#from usuarios.router import oauth2_scheme
import anecdotas.models as models 
import anecdotas.schemas as schemas
import anecdotas.service as service

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

@router.get('', response_model=list[schemas.Anecdota])
def listar_anecdotas(db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)):
    return service.listar_anecdotas(db=db)

@router.get('/reseña/{id}', response_model=list[schemas.Anecdota])
def listar_anectodas(id: int, db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)):
    return service.listar_anecdotas_reseñas(id=id, db=db)

@router.post('')
def crear_anecdota(nombre: str = Form(...), 
                   descripcion: str = Form(...), 
                   reseña: int = Form(...), 
                   actual: int = Form(...), 
                   db: Session = Depends(get_db), 
                   info=Depends(auth_handler.auth_wrapper)):
    anecdota = schemas.AnecdotaCrear(
        nombre=nombre, 
        descripcion=descripcion, 
        reseña_id=reseña
    )
    service.crear_anecdota(db=db, anecdota=anecdota)
    return RedirectResponse(url=f'/productos/{actual}', status_code=status.HTTP_303_SEE_OTHER)

@router.get('/{id}', response_model=schemas.Anecdota)
def buscar_anecdota(id : int, db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)): 
    return service.buscar_anecdota(db=db, id=id)

@router.put('/{id}', response_model=schemas.Anecdota)
def modificar_anecdota(id : int, anecdota: schemas.AnecdotaCrear, db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)): 
    return service.modificar_anecdota(db=db, id=id, anecdota=anecdota)

@router.delete('/{id}', response_model=schemas.Anecdota)
def eliminar_anecdota(id : int, db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)): 
    return service.eliminar_anecdota(db=db, id=id)