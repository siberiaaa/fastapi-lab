from fastapi import APIRouter, Depends, Request, Form, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import compras.models as models 
import compras.schemas as schemas
import compras.service as service

from usuarios.service import AuthHandler
from exceptions import No_Cliente_Exception, No_Artesano_Exception, Message_Redirection_Exception

auth_handler = AuthHandler()

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

templates = Jinja2Templates(directory="../templates")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/pedido/crear')
def crear_pedido(request: Request, info=Depends(auth_handler.auth_wrapper)):
    if info["tipo_usuario_id"] != 2: 
             raise No_Cliente_Exception()
    return templates.TemplateResponse(request=request, name="pedidos/crear_pedidos.html")  

@router.get('/encargo/crear')
def crear_encargo(request: Request, info=Depends(auth_handler.auth_wrapper)):
    if info["tipo_usuario_id"] != 2: 
             raise No_Cliente_Exception()
    return templates.TemplateResponse(request=request, name="encargos/crear_pedidos.html")  

# cantidad: int
#     fecha: Union[datetime, None] = None
#     cliente_cedula: str
#     producto_id: int
#     tipo_compra_id: int
#     estado_compra_id: Union[int, None] = None
# --------------------


@router.get('', response_model=list[schemas.Compra])
def listar_compras(db: Session = Depends(get_db)):
    return service.listar_compras(db=db)


@router.post('', response_model=schemas.Compra)
def crear_compra(compra: schemas.CompraCrear, db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)):
    return service.realizar_compra(db=db, compra=compra)

@router.get('/{id}', response_model=schemas.Compra)
def buscar_compra(id : int, db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)): 
    return service.get_compra(db=db, id=id)

@router.put('/{id}', response_model=schemas.Compra)
def modificar_compra(id : int, compra: schemas.CompraCrear, db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)): 
    return service.modificar_compra(db=db, id=id, compra=compra)

@router.delete('/{id}', response_model=schemas.Compra)
def eliminar_compra(id : int, db: Session = Depends(get_db)): 
    return service.eliminar_compra(db=db, id=id)