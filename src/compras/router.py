from fastapi import APIRouter, Depends, Request, Form, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from datetime import datetime
import compras.models as models 
import compras.schemas as schemas
import compras.service as service

import productos.service as producto_service
import cotizaciones.service as cotizacion_service
import cotizaciones.schemas as cotizacion_schema

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
def crear_pedido(request: Request, db : Session = Depends(get_db), product_id: int = -1, info=Depends(auth_handler.auth_wrapper)):
    if product_id == -1:
         raise Message_Redirection_Exception(message='Link de compra inválido', path_message='Volver a inicio', path_route='/')
    if info["tipo_usuario_id"] != 2: 
             raise No_Cliente_Exception()
    producto = producto_service.get_producto(db=db, id=product_id)
    return templates.TemplateResponse(request=request, name="compras/crear_pedidos.html", context={
         'cedula_cliente': info['cedula'], 
         'producto_id':product_id, 
         'info': info, 
         'producto': producto.data})  

@router.post('/pedido/crear')
def crear_encargo(request: Request, db: Session = Depends(get_db),
                      cedula: str = Form(...), 
                      id_producto: int = Form(...), 
                      cantidad: int = Form(...), 
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
        return templates.TemplateResponse("message-redirection.html", {
             "request": request, 
             "message": 'Pedido realizado correctamente', 
             "path_route": '/home', 
             "path_message": 'Volver a home', 
             'info': info})
    else:
        raise Message_Redirection_Exception(message=respuesta.mensaje, path_message='Volver a home', path_route='/home')


@router.get('/encargo/crear')
def crear_encargo(request: Request, product_id: int = -1, info=Depends(auth_handler.auth_wrapper)):
    if product_id == -1:
         raise Message_Redirection_Exception(message='Link de compra inválido', path_message='Volver a inicio', path_route='/')
    if info["tipo_usuario_id"] != 2: 
             raise No_Cliente_Exception()
    
    return templates.TemplateResponse(request=request, name="compras/crear_encargos.html", context={
         'cedula_cliente': info['cedula'], 
         'producto_id':product_id, 
         'info': info})  

@router.post('/encargo/crear')
def crear_encargo(request: Request, db: Session = Depends(get_db),
                      cedula: str = Form(...), 
                      id_producto: int = Form(...), 
                      cantidad: int = Form(...), 
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


@router.get('')
def ver_compras(request: Request, info=Depends(auth_handler.auth_wrapper)):
    if info["tipo_usuario_id"] == 1:
         return RedirectResponse(url='/compras/artesano', status_code=status.HTTP_303_SEE_OTHER)
    
    if info["tipo_usuario_id"] == 2:
         return RedirectResponse(url='/compras/cliente', status_code=status.HTTP_303_SEE_OTHER)


# cliente gestion compra #
@router.get('/cliente')
def ver_compras_artesano(request: Request, info=Depends(auth_handler.auth_wrapper), db: Session = Depends(get_db)):
    if info["tipo_usuario_id"] != 2: 
             raise No_Cliente_Exception
    
    respuesta = service.listar_compras_para_cliente(db=db, cedula=info['cedula'])

    if (respuesta.ok):
        return templates.TemplateResponse(request=request, name="compras/ver_compras_cliente.html", context={
             'compras':respuesta.data, 
             'info': info})  
    else:
        raise Message_Redirection_Exception(message=respuesta.mensaje, path_message='Volver a home', path_route='/home')
    

# artesano gestion compra #
@router.get('/artesano')
def ver_compras_artesano(request: Request, info=Depends(auth_handler.auth_wrapper), db: Session = Depends(get_db)):
    if info["tipo_usuario_id"] != 1: 
             raise No_Artesano_Exception
    
    respuesta = service.listar_compras_para_artesano(db=db, cedula=info['cedula'])
    

    if (respuesta.ok):
        return templates.TemplateResponse(request=request, name="compras/ver_compras_artesano.html", context={
             'compras':respuesta.data, 
             'info': info})  
    else:
        raise Message_Redirection_Exception(message=respuesta.mensaje, path_message='Volver a home', path_route='/home')
    
@router.get('/artesano/{id_compra}')
def revisar_compra_artesano(id_compra: int, request: Request, db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)):
    if info["tipo_usuario_id"] != 1: 
             raise No_Artesano_Exception
    
    respuesta = service.get_compra(db=db, id=id_compra)
    print(respuesta)
    if not respuesta.ok:
         raise Message_Redirection_Exception(message=respuesta.mensaje, path_message='Volver a home', path_route='/home')
    
    producto_respuesta = producto_service.get_producto(db=db, id=respuesta.data.producto_id)
    print(producto_respuesta)
    if not producto_respuesta.ok:
         raise Message_Redirection_Exception(message=producto_respuesta.mensaje, path_message='Volver a home', path_route='/home')

    return templates.TemplateResponse(request=request, name="compras/revisar_compra_artesano.html", context={
         'compra':respuesta.data, 
         'producto':producto_respuesta.data, 
         'info': info})  

@router.post('/artesano/{id_compra}')
def revisar_compra_artesano_cotizar(request: Request, id_compra: int,  cotizar: bool = Form(...), precio: float = Form(...), cantidad: int = Form(...), info=Depends(auth_handler.auth_wrapper), db: Session = Depends(get_db)):
    if info["tipo_usuario_id"] != 1: 
             raise No_Artesano_Exception
    
    #
    #!Validacion del form para encargos no implementado (y mucho menos la aprobacion de caracteristicas)
    #
    if not cotizar:
         respuesta =  service.rechazar_compra(db=db, id_compra=id_compra)
         if (respuesta.ok):
            return templates.TemplateResponse("message-redirection.html", {"request": request, "message": 'Compra rechazada correctamente', "path_route": '/home', "path_message": 'Volver a home'})
         else:
            raise Message_Redirection_Exception(message=respuesta.mensaje, path_message='Volver a home', path_route='/home')
        
    #modificar a aprobar
    respuesta_aprobar =  service.aprobar_compra(db=db, id_compra=id_compra)
    if not respuesta_aprobar.ok:
         raise Message_Redirection_Exception(message=respuesta_aprobar.mensaje, path_message='Volver a home', path_route='/home')

    #modificar la cantidad de la compra
    respuesta_modificar = service.modificar_cantidad_compra(db=db, id_compra=id_compra, cantidad=cantidad)
    if not respuesta_modificar.ok:
         raise Message_Redirection_Exception(message=respuesta_modificar.mensaje, path_message='Volver a home', path_route='/home')

    #resto de flujo de cosas que deberían suceder
    cotizacion = cotizacion_schema.CotizacionCrear(
                            compra_id=id_compra,
                            precio=precio, 
                            estado_cotizacion_id=1) 
    
    respuesta = cotizacion_service.crear_cotizacion(db=db, cotizacion=cotizacion)

    if (respuesta.ok):
        return templates.TemplateResponse("message-redirection.html", {"request": request, "message": 'Cotizacion enviada correctamente', "path_route": '/home', "path_message": 'Volver a home'})
    else:
        raise Message_Redirection_Exception(message=respuesta.mensaje, path_message='Volver a home', path_route='/home')
    


# @router.get('', response_model=list[schemas.Compra])
# def listar_compras(db: Session = Depends(get_db)):
#     return service.listar_compras(db=db)


# @router.post('', response_model=schemas.Compra)
# def crear_compra(compra: schemas.CompraCrear, db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)):
#     return service.realizar_compra(db=db, compra=compra)

# @router.get('/{id}', response_model=schemas.Compra)
# def buscar_compra(id : int, db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)): 
#     return service.get_compra(db=db, id=id)

@router.put('/{id}', response_model=schemas.Compra)
def modificar_compra(id : int, compra: schemas.CompraCrear, db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)): 
    return service.modificar_compra(db=db, id=id, compra=compra)

@router.delete('/{id}', response_model=schemas.Compra)
def eliminar_compra(id : int, db: Session = Depends(get_db)): 
    return service.eliminar_compra(db=db, id=id)

#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa prueba prueba
@router.post('/check')
async def check(request: Request):
    da = await request.form()
    da = jsonable_encoder(da)
    print(da)
    return da