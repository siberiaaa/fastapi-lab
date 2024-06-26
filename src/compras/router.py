from fastapi import APIRouter, Depends, Request, Form, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from datetime import datetime
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
def crear_pedido(request: Request, product_id: int = -1, info=Depends(auth_handler.auth_wrapper)):
    if product_id == -1:
         raise Message_Redirection_Exception(message='Link de compra inválido', path_message='Volver a inicio', path_route='/')
    if info["tipo_usuario_id"] != 2: 
             raise No_Cliente_Exception()
    
    return templates.TemplateResponse(request=request, name="compras/crear_pedidos.html")  

@router.post('/pedido/crear')
def crear_encargo(request: Request, db: Session = Depends(get_db),
                      cedula: str = Form(...), 
                      id_producto: int = Form(...), 
                      cantidad: int = Form(...), 
                      fecha: datetime = Form(...), 
                      info=Depends(auth_handler.auth_wrapper)):
    
    if info["tipo_usuario_id"] != 2: 
             raise No_Cliente_Exception()
    
    compra = schemas.CompraCrear(
                            fecha = datetime.now(),
                            cantidad=cantidad, 
                            cliente_cedula=cedula, 
                            producto_id=id_producto, 
                            tipo_compra_id=1, 
                            estado_compra_id=1) 
    
    respuesta = service.realizar_compra(db=db, compra=compra)
    
    if (respuesta.ok):
        return templates.TemplateResponse("message-redirection.html", {"request": request, "message": 'Pedido realizado correctamente', "path_route": '/home', "path_message": 'Volver a home'})
    else:
        raise Message_Redirection_Exception(message=respuesta.mensaje, path_message='Volver a home', path_route='/home')


@router.get('/encargo/crear')
def crear_encargo(request: Request, product_id: int = -1, info=Depends(auth_handler.auth_wrapper)):
    if product_id == -1:
         raise Message_Redirection_Exception(message='Link de compra inválido', path_message='Volver a inicio', path_route='/')
    if info["tipo_usuario_id"] != 2: 
             raise No_Cliente_Exception()
    
    return templates.TemplateResponse(request=request, name="compras/crear_encargos.html", context={'cedula_cliente':info['cedula'], 'producto_id': product_id, 'fecha': datetime.now()})  

@router.post('/encargo/crear')
def crear_encargo(request: Request, db: Session = Depends(get_db),
                      cedula: str = Form(...), 
                      id_producto: int = Form(...), 
                      cantidad: int = Form(...), 
                      fecha: datetime = Form(...), 
                      info=Depends(auth_handler.auth_wrapper)):
    
    if info["tipo_usuario_id"] != 2: 
             raise No_Cliente_Exception()
    
    compra = schemas.CompraCrear(
                            fecha = datetime.now(),
                            cantidad=cantidad, 
                            cliente_cedula=cedula, 
                            producto_id=id_producto, 
                            tipo_compra_id=2, 
                            estado_compra_id=1) 
    
    respuesta = service.realizar_compra(db=db, compra=compra)

    if (respuesta.ok):
        return templates.TemplateResponse("message-redirection.html", {"request": request, "message": 'Encargo realizado correctamente', "path_route": '/home', "path_message": 'Volver a home'})
    else:
        raise Message_Redirection_Exception(message=respuesta.mensaje, path_message='Volver a home', path_route='/home')


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