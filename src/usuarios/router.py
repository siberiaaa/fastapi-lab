from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from datetime import timedelta
from sqlalchemy.orm import Session
from database import SessionLocal, engine 
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from datetime import datetime
from fastapi.responses import RedirectResponse, HTMLResponse, Response
from tipos_usuario.service import listar_tipos_usuarios

from schemas import Token, Respuesta

import usuarios.models as models 
import usuarios.schemas as schemas
# import usuarios.service as service
from usuarios.service import AuthHandler, RequiresLoginException, eliminar_usuario

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="iniciar_sesion") comentado en repo

auth_handler = AuthHandler()

templates = Jinja2Templates(directory="../templates/usuarios")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#creo que tambien va para el main esto
# redirection block (este handler redirecciona a iniciar sesion si ocurre la excepción blabalbla)
# @router.exception_handler(RequiresLoginException)
# async def exception_handler(request: Request, exc: RequiresLoginException) -> Response:
#     return RedirectResponse(url='/iniciar_sesion')        

#!Creo que ese middleware va en el main por eso lo dejé por allá
# @router.middleware("http")
# async def create_auth_header(request: Request, call_next,):
#     '''
#     Check if there are cookies set for authorization. If so, construct the
#     Authorization header and modify the request (unless the header already
#     exists!)
#     '''
#     if ("Authorization" not in request.headers 
#         and "Authorization" in request.cookies
#         ):
#         access_token = request.cookies["Authorization"]
        
#         request.headers.__dict__["_list"].append(
#             (
#                 "authorization".encode(),
#                  f"Bearer {access_token}".encode(),
#             )
#         )
#     elif ("Authorization" not in request.headers 
#         and "Authorization" not in request.cookies
#         ): 
#         request.headers.__dict__["_list"].append(
#             (
#                 "authorization".encode(),
#                  f"Bearer 12345".encode(),
#             )
#         )
        
#     response = await call_next(request)
#     return response    



@router.get('/registrar', response_class=HTMLResponse)
def registrar_usuario(request: Request, db: Session = Depends(get_db)):
    lista = listar_tipos_usuarios(db=db)
    return templates.TemplateResponse("registrar.html", {'request': request, 'lista': lista})      

@router.post('/registrar', response_class=HTMLResponse)
def registrar_usuario(request: Request, 
                      cedula: str = Form(...), 
                      nombres: str = Form(...), 
                      apellidos: str = Form(...), 
                      direccion: str = Form(...), 
                      nacimiento: datetime = Form(...), 
                      correo: str = Form(...), 
                      contraseña: str = Form(...), 
                      tipo_id: int = Form(...), 
                      db: Session = Depends(get_db)):

    usuario = schemas.Usuario(
        cedula=cedula, 
        nombres=nombres, 
        apellidos=apellidos, 
        direccion=direccion, 
        nacimiento=nacimiento, 
        correo=correo, 
        contraseña=contraseña, 
        tipo_id=tipo_id
    )
    auth_handler.registrar_usuario(db=db, usuario=usuario)
    return RedirectResponse(url='/', status_code=status.HTTP_303_SEE_OTHER)


@router.get('/iniciar_sesion', response_class=HTMLResponse)
def registrar_usuario(request: Request):
    return templates.TemplateResponse(request=request, name="iniciarsesion.html")      

#def iniciar_sesion(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)): 
@router.post('/iniciar_sesion')
async def iniciar_sesion(request: Request, response: Response, cedula: str = Form(...), contraseña: str = Form(...),db: Session = Depends(get_db)) -> Token: 
    usuario = await auth_handler.authenticate_user(db, cedula, contraseña)
    try:
        if usuario: 
            nombre_completo = f'{usuario.nombres} {usuario.apellidos}'
            atoken = auth_handler.create_access_token(data={'cedula': usuario.cedula, 'nombre_completo': nombre_completo, 'tipo_usuario_id': usuario.tipo_id})
            if usuario.tipo_id == 1: 
                response = templates.TemplateResponse("success.html", 
                    {"request": request, "nombre_completo": nombre_completo, "success_msg": "Bienvenido, ve a tu página de inicio ",
                    "path_route": '/home', "path_msg": "Home"})
            elif usuario.tipo_id == 2: 
                response = templates.TemplateResponse("success.html", 
                    {"request": request, "nombre_completo": nombre_completo, "success_msg": "Bienvenido, ve a tu página de inicio ",
                    "path_route": '/home', "path_msg": "Home"})
            else: 
                response = templates.TemplateResponse("success.html", 
                    {"request": request, "nombre_completo": nombre_completo, "success_msg": "Bienvenido, ve a tu página de inicio ",
                    "path_route": '/home', "path_msg": "Home"})
            
            response.set_cookie(key="Authorization", value= f"{atoken}", httponly=True)
            return response
        else:
                return templates.TemplateResponse("error.html",
                {"request": request, 'detail': 'Incorrect Username or Password', 'status_code': 404 })

    except Exception as err:
        return templates.TemplateResponse("error.html",
            {"request": request, 'detail': 'Incorrect Username or Password', 'status_code': 401 })
        
@router.get('/logout')
async def logout(request: Request, response: Response):
    response = templates.TemplateResponse("success.html", 
                    {"request": request, "nombre_completo": "", "success_msg": "Hasta luego vuelve pronto",
                    "path_route": '/', "path_msg": "Inicio"})
    response.delete_cookie(key="Authorization")
    return response

#prueba prueba 
@router.get("/private", response_class=HTMLResponse)
async def private(request: Request, info=Depends(auth_handler.auth_wrapper)):
    try:
        return templates.TemplateResponse("private.html", {"request": request, "info": info})
    except:
        raise RequiresLoginException() 
    
    # RedirectResponse(url='/', status_code=status.HTTP_303_SEE_OTHER)
    # return Token(access_token=token_acceso, token_type='bearer')


@router.delete('/usuario/{cedula}', response_model=schemas.Usuario)
def borrar_usuario(cedula : str, db: Session = Depends(get_db)): 
    return eliminar_usuario(db=db, cedula=cedula)

