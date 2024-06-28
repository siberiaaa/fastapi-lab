from fastapi import APIRouter, Depends, Request, Form, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import cotizaciones.models as models 
import cotizaciones.schemas as schemas
import cotizaciones.service as service
from schemas import Respuesta

import compras.service as compra_service
import productos.service as producto_service

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

# cliente gestion cotizaciones #
@router.get('/cliente')
def ver_cotizaciones_cliente(request: Request, info=Depends(auth_handler.auth_wrapper), db: Session = Depends(get_db)):
    if info["tipo_usuario_id"] != 2: 
             raise No_Cliente_Exception
    
    respuesta = service.listar_cotizaciones_para_cliente(db=db, cedula=info['cedula'])

    if (respuesta.ok):
        return templates.TemplateResponse(request=request, name="cotizaciones/ver_cotizaciones_cliente.html", context={'cotizaciones':respuesta.data})  
    else:
        raise Message_Redirection_Exception(message=respuesta.mensaje, path_message='Volver a home', path_route='/home')
    
@router.get('/cliente/{id_cotizacion}')
def revisar_compra_cliente(id_cotizacion: int, request: Request, info=Depends(auth_handler.auth_wrapper), db: Session = Depends(get_db)):
    if info["tipo_usuario_id"] != 2: 
             raise No_Cliente_Exception
    
    #cotizacion
    cotizacion_respuesta = service.buscar_cotizacion(db=db, id=id_cotizacion)
    if not cotizacion_respuesta.ok:
         raise Message_Redirection_Exception(message=cotizacion_respuesta.mensaje, path_message='Volver a home', path_route='/home')

    #compra
    compra_respuesta = compra_service.get_compra(db=db, id=cotizacion_respuesta.data.compra_id)
    if not compra_respuesta.ok:
         raise Message_Redirection_Exception(message=compra_respuesta.mensaje, path_message='Volver a home', path_route='/home')
    
    #producto
    producto_respuesta = producto_service.get_producto(db=db, id=compra_respuesta.data.producto_id)
    if not producto_respuesta.ok:
         raise Message_Redirection_Exception(message=producto_respuesta.mensaje, path_message='Volver a home', path_route='/home')
  
    return templates.TemplateResponse(request=request, name="cotizaciones/revisar_cotizacion_cliente.html", context={'cotizacion':cotizacion_respuesta.data, 'compra':compra_respuesta.data, 'producto':producto_respuesta.data})  
   
@router.post('/cliente/{id_cotizacion}')
def revisar_compra_cliente_facturar(request: Request, id_cotizacion: int,  pedir_factura: bool = Form(...), info=Depends(auth_handler.auth_wrapper), db: Session = Depends(get_db)):
    if info["tipo_usuario_id"] != 2: 
             raise No_Cliente_Exception
    
    if not pedir_factura:
         respuesta =  service.rechazar_cotizacion(db=db, id_cotizacion=id_cotizacion)
         if (respuesta.ok):
            return templates.TemplateResponse("message-redirection.html", {"request": request, "message": 'Cotización rechazada correctamente', "path_route": '/home', "path_message": 'Volver a home'})
         else:
            raise Message_Redirection_Exception(message=respuesta.mensaje, path_message='Volver a home', path_route='/home')
         
    respuesta =  service.aprobar_cotizacion(db=db, id_cotizacion=id_cotizacion)
    if (respuesta.ok):
        return templates.TemplateResponse("message-redirection.html", {"request": request, "message": 'Cotización aprobada correctamente', "path_route": '/home', "path_message": 'Volver a home'})
    else:
        raise Message_Redirection_Exception(message=respuesta.mensaje, path_message='Volver a home', path_route='/home')
    

@router.get('')
def ver_cotizaciones(request: Request, info=Depends(auth_handler.auth_wrapper)):
    if info["tipo_usuario_id"] == 1:
         return RedirectResponse(url='/cotizaciones/artesano', status_code=status.HTTP_303_SEE_OTHER)
    
    if info["tipo_usuario_id"] == 2:
         return RedirectResponse(url='/cotizaciones/cliente', status_code=status.HTTP_303_SEE_OTHER)


# artesano gestion cotizaciones #
@router.get('/artesano')
def ver_cotizaciones_artesano(request: Request, info=Depends(auth_handler.auth_wrapper), db: Session = Depends(get_db)):
    if info["tipo_usuario_id"] != 1: 
             raise No_Artesano_Exception
    
    respuesta = service.listar_cotizaciones_para_artesanos(db=db, cedula=info['cedula'])

    if (respuesta.ok):
        return templates.TemplateResponse(request=request, name="cotizaciones/ver_cotizaciones_artesano.html", context={'cotizaciones':respuesta.data})  
    else:
        raise Message_Redirection_Exception(message=respuesta.mensaje, path_message='Volver a home', path_route='/home')
    
    

@router.get('', response_model=list[schemas.Cotizacion])
def listar_cotizaciones(db: Session = Depends(get_db)):
    return service.listar_cotizaciones(db=db)

@router.get('/compra/{id}', response_model=Respuesta[list[schemas.Cotizacion]])
def listar_cotizaciones(id: int, db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)):
    return service.listar_cotizaciones_compras(db=db, id=id)

@router.post('/aprobar/{id}', response_model=Respuesta[schemas.Cotizacion])
def aprobar_cotizacion(id: int, db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)):
    return service.aprobar_cotizacion(db=db, id=id)

@router.get('/solicitar/{id}')
def solicitar_cotizacion(request: Request, 
                    nombre: str = Form(...), 
                    descripcion: str = Form(...), 
                    db: Session = Depends(get_db),
                    info=Depends(auth_handler.auth_wrapper)):
    
    if info["tipo_usuario_id"] != 2: 
             raise No_Cliente_Exception()
    
    # categoria = schemas.CotizacionCrear(nombre=nombre, descripcion=descripcion) 
    # respuesta = service.create_categoria(db=db, categoria=categoria)

    # if (respuesta.ok):
    #     return RedirectResponse(url='/categorias', status_code=status.HTTP_303_SEE_OTHER)
    # else:
    #      raise Message_Redirection_Exception(message=respuesta.mensaje, path_message='Volver a categorias', path_route='/categorias')


@router.post('', response_model=Respuesta[schemas.Cotizacion])
def solicitar_cotizacion(cotizacion=schemas.CotizacionCrear, db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)):
    return service.crear_cotizacion(db=db, cotizacion=cotizacion)

@router.post('/rechazar/{id}', response_model=Respuesta[schemas.Cotizacion])
def rechazar_cotizacion(id: int, db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)):
    return service.rechazar_cotizacion(db=db, id=id)

@router.get('/{id}', response_model=Respuesta[schemas.Cotizacion])
def buscar_cotizacion(id : int, db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)): 
    return service.buscar_cotizacion(db=db, id=id)

@router.put('/{id}', response_model=schemas.Cotizacion)
def modificar_cotizacion(id : int, cotizacion: schemas.CotizacionCrear, db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)): 
    return service.modificar_cotizacion(db=db, id=id, cotizacion=cotizacion)

@router.delete('/{id}', response_model=schemas.Cotizacion)
def eliminar_cotizacion(id : int, db: Session = Depends(get_db)): 
    return service.eliminar_cotizacion(db=db, id=id)