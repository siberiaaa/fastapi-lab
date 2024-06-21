from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from jose import jwt
from database import SessionLocal, engine
from schemas import Respuesta
import categorias.models as models
import categorias.schemas as schemas
import categorias.service as service

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

@router.get('', response_model=Respuesta[list[schemas.Categoria]])
def get_categorias(db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)):
        return service.get_categorias(db=db)

@router.post('', response_model=Respuesta[schemas.Categoria])
def crear_categoria(categoria: schemas.CategoriaCrear, db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)):
    return service.create_categoria(db=db, categoria=categoria)

@router.get('/{categoria_id}', response_model=Respuesta[schemas.Categoria])
def get_categoria(categoria_id: int, db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)):
    return service.get_categoria(db=db, categoria_id=categoria_id)

@router.put('/{categoria_id}', response_model=Respuesta[schemas.Categoria])
def update_categoria(categoria_id: int, categoria: schemas.CategoriaCrear, db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)):
    return service.update_categoria(db=db, categoria_id=categoria_id, categoria=categoria)

@router.delete('/{categoria_id}', response_model=Respuesta[schemas.Categoria])
def delete_categoria(categoria_id: int, db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)):
    return service.delete_categoria(db=db, categoria_id=categoria_id)


