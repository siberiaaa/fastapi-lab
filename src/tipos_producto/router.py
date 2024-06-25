from fastapi import APIRouter, Depends, Request, Form, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from schemas import Respuesta
import tipos_producto.models as models 
import tipos_producto.schemas as schemas
import tipos_producto.service as service

from usuarios.service import AuthHandler
from exceptions import No_Artesano_Exception, Message_Redirection_Exception

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

@router.get('')
def get_tipos_productos(request: Request, db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)):
    if info["tipo_usuario_id"] != 1: 
             raise No_Artesano_Exception()
        
    lista_tipos_respuesta = service.get_tipos_producto(db=db)

    if (lista_tipos_respuesta.ok):
        return templates.TemplateResponse(request=request, name="tipos_productos/ver_tipos.html", context={"tipos":lista_tipos_respuesta.data})
    else:
        raise Message_Redirection_Exception(message=lista_tipos_respuesta.mensaje, path_message='Volver a inicio', path_route='/')

@router.get('/crear')
def crear_tipos_productos(request: Request, info=Depends(auth_handler.auth_wrapper)):
    if info["tipo_usuario_id"] != 1: 
             raise No_Artesano_Exception()
    return templates.TemplateResponse(request=request, name="tipos_productos/crear_tipos.html")  

@router.post('/crear')
def crear_tipos_productos(request: Request, 
                    nombre: str = Form(...), 
                    descripcion: str = Form(...), 
                    funcionalidad: bool = Form(...), 
                    db: Session = Depends(get_db),
                    info=Depends(auth_handler.auth_wrapper)):
    
    if info["tipo_usuario_id"] != 1: 
             raise No_Artesano_Exception()
    
    tipo_producto = schemas.Tipo_ProductoCrear(nombre=nombre, descripcion=descripcion, funcionalidad=funcionalidad) 
    respuesta = service.create_tipo_producto(db=db, tipo_producto=tipo_producto)

    if (respuesta.ok):
        return RedirectResponse(url='/tipos_productos', status_code=status.HTTP_303_SEE_OTHER)
    else:
         raise Message_Redirection_Exception(message=respuesta.mensaje, path_message='Volver a tipos de producto', path_route='/tipos_productos')



@router.delete('/{id}')
def eliminar_tipo_producto(id: int, db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)): 
    if info["tipo_usuario_id"] != 1: 
             raise No_Artesano_Exception()
    respuesta = service.delete_tipo_producto(db=db, id=id)
    if (respuesta.ok):
        return RedirectResponse(url='/tipos_productos', status_code=status.HTTP_303_SEE_OTHER)
    else:
         raise Message_Redirection_Exception(message=respuesta.mensaje, path_message='Volver a tipos de producto', path_route='/tipos_productos')




# Uso interno #

@router.get('/{id}', response_model=Respuesta[schemas.Tipo_Producto])
def get_tipo_producto(id: int, db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)): 
    return service.get_tipo_producto(db=db, id=id)

@router.put('/{id}', response_model=Respuesta[schemas.Tipo_Producto])
def update_tipo_producto(id: int, tipo_producto: schemas.Tipo_ProductoCrear, db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)): 
    return service.update_tipo_producto(db=db, id=id, tipo_producto=tipo_producto)

