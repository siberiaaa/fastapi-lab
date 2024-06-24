from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from jose import jwt
from database import SessionLocal, engine
from schemas import Respuesta
import categorias.models as models
import categorias.schemas as schemas
import categorias.service as service

from usuarios.service import AuthHandler
from exceptions import No_Artesano_Exception
auth_handler = AuthHandler()

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

templates = Jinja2Templates(directory="../templates/categorias")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('', response_class=HTMLResponse)
def get_categorias(request: Request, db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)):
        if info["tipo_usuario_id"] != 1: 
             raise No_Artesano_Exception()
        lista_categorias_respuesta = service.get_categorias(db=db)
        return templates.TemplateResponse(request=request, name="ver_categorias.html", categorias=lista_categorias_respuesta.data)

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


