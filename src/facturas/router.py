from fastapi import APIRouter, Depends, Request, Form, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import facturas.models as models 
import facturas.schemas as schemas
import facturas.service as service
from schemas import Respuesta
from datetime import datetime

import cotizaciones.service as cotizacion_service
import compras.service as compra_service
import productos.service as producto_service
import metodos_envios.service as envio_service
import metodos_pagos.service as pago_service

from exceptions import No_Artesano_Exception, No_Cliente_Exception, Message_Redirection_Exception

from usuarios.service import AuthHandler
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

# 

@router.get('')
def ver_facturas(request: Request, info=Depends(auth_handler.auth_wrapper)):
    if info["tipo_usuario_id"] == 1:
         return RedirectResponse(url='/facturas/artesano', status_code=status.HTTP_303_SEE_OTHER)
    
    if info["tipo_usuario_id"] == 2:
         return RedirectResponse(url='/facturas/cliente', status_code=status.HTTP_303_SEE_OTHER)
    
# cliente gestion facturas #
@router.get('/cliente')
def ver_facturas_cliente(request: Request, info=Depends(auth_handler.auth_wrapper), db: Session = Depends(get_db)):
    if info["tipo_usuario_id"] != 2: 
             raise No_Cliente_Exception
    
    respuesta = service.listar_facturas_cliente(db=db, cedula=info['cedula'])

    if (respuesta.ok):
        return templates.TemplateResponse(request=request, name="facturas/ver_facturas_usuarios.html", context={'facturas':respuesta.data, 'tipo_usuario': info["tipo_usuario_id"]})  
    else:
        raise Message_Redirection_Exception(message=respuesta.mensaje, path_message='Volver a home', path_route='/home')

# artesano gestion facturas #
@router.get('/artesano')
def ver_facturas_artesano(request: Request, info=Depends(auth_handler.auth_wrapper), db: Session = Depends(get_db)):
    if info["tipo_usuario_id"] != 1: 
             raise No_Artesano_Exception
    
    respuesta = service.listar_facturas_artesano(db=db, cedula=info['cedula'])

    if (respuesta.ok):
        return templates.TemplateResponse(request=request, name="facturas/ver_facturas_usuarios.html", context={'facturas':respuesta.data, 'tipo_usuario': info["tipo_usuario_id"]})  
    else:
        raise Message_Redirection_Exception(message=respuesta.mensaje, path_message='Volver a home', path_route='/home')

@router.get('/artesano/{id_cotizacion}')
def realizar_facturar_artesano(id_cotizacion: int, request: Request, info=Depends(auth_handler.auth_wrapper), db: Session = Depends(get_db)):
    if info["tipo_usuario_id"] != 1: 
             raise No_Artesano_Exception

    #metodos envio
    envio_respuesta = envio_service.listar_metodos_envios(db=db)
    if not envio_respuesta.ok:
         raise Message_Redirection_Exception(message=envio_respuesta.mensaje, path_message='Volver a home', path_route='/home')
    
    #metodos pago
    pago_respuesta = pago_service.listar_metodos_pagos(db=db)
    if not pago_respuesta.ok:
         raise Message_Redirection_Exception(message=pago_respuesta.mensaje, path_message='Volver a home', path_route='/home')
  
    return templates.TemplateResponse(request=request, name="facturas/realizar_factuas_artesano.html", context={'id_cotizacion':id_cotizacion, 'metodos_envio':envio_respuesta.data, 'metodos_pago':pago_respuesta.data})  
   
@router.post('/artesano/{id_cotizacion}')
def realizar_facturar_artesano(request: Request, id_cotizacion: int,
                              entrega: datetime = Form(...), 
                              envio: int = Form(...), 
                              pago: int = Form(...), 
                              info=Depends(auth_handler.auth_wrapper), db: Session = Depends(get_db)):
    if info["tipo_usuario_id"] != 1: 
             raise No_Artesano_Exception
    
    cotizacion_respuesta = cotizacion_service.aprobar_facturada_cotizacion(db=db, id_cotizacion=id_cotizacion)
    if not cotizacion_respuesta.ok:
         raise Message_Redirection_Exception(message=cotizacion_respuesta.mensaje, path_message='Volver a home', path_route='/home')

    envio_respuesta = envio_service.listar_metodos_envios(db=db)
    if not envio_respuesta.ok:
         raise Message_Redirection_Exception(message=envio_respuesta.mensaje, path_message='Volver a home', path_route='/home')
    

    factura = schemas.FacturaCrear(fecha_entrega=entrega, cotizacion_id=id_cotizacion, metodo_envio_id=envio, metodo_pago_id=pago)
    respuesta =  service.crear_factura(db=db, factura=factura)
    if (respuesta.ok):
        return templates.TemplateResponse("message-redirection.html", {"request": request, "message": 'Factura creada correctamente', "path_route": '/home', "path_message": 'Volver a home'})
    else:
        raise Message_Redirection_Exception(message=respuesta.mensaje, path_message='Volver a home', path_route='/home')
    





#@router.get('', response_model=list[schemas.Factura])
# def listar_facturas(db: Session = Depends(get_db)):
#     return service.listar_facturas(db=db)

# @router.get('/cotizacion/{id}', response_model=Respuesta[list[schemas.Factura]])
# def listar_facturas_cotizacion(id: int, db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)):
#     return service.listar_facturas_cotizaciones(db=db, id=id)

# @router.post('', response_model=schemas.Factura)
# def crear_factura(factura: schemas.FacturaCrear, db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)):
#     return service.crear_factura(db=db, factura=factura)

# @router.get('/{id}', response_model=schemas.Factura)
# def buscar_factura(id : int, db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)): 
#     return service.buscar_factura(db=db, id=id)


# @router.put('/{id}', response_model=schemas.Factura)
# def modificar_factura(id : int, factura: schemas.FacturaCrear, db: Session = Depends(get_db)): 
#     return service.modificar_factura(db=db, id=id, factura=factura)

# @router.delete('/{id}', response_model=schemas.Factura)
# def eliminar_factura(id : int, db: Session = Depends(get_db)): 
#     return service.eliminar_factura(db=db, id=id)