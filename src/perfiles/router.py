from fastapi import Request, Depends, APIRouter
from database import SessionLocal 
from fastapi.templating import Jinja2Templates
from usuarios.service import AuthHandler
from sqlalchemy.orm import Session
from usuarios.service import buscar_usuario
import perfiles.service as service

auth_handler = AuthHandler()

router = APIRouter()

templates = Jinja2Templates(directory="../templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/perfil')
def perfil(request: Request, db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)):
        print(info)
        usuario = buscar_usuario(db=db, cedula=info['cedula'])
        print(usuario)
        if info["tipo_usuario_id"] == 1: 
            lista = service.listar_compras_cliente(db=db, cedula=info['cedula'])
            return templates.TemplateResponse('/perfiles/clientes.html', 
                                              {'request': request, 
                                               "usuario": usuario.data, 
                                               'lista': lista})
        elif info["tipo_usuario_id"] == 2: 
            lista = service.listar_compras_artesano(db=db, cedula=info['cedula'])
            return templates.TemplateResponse('/perfiles/artesanos.html', 
                                              {'request': request, 
                                               "usuario": usuario.data, 
                                               'lista': lista})
        else: 
            return {'hola': info}