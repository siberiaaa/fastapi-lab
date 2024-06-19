from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from datetime import timedelta
from sqlalchemy.orm import Session
from database import SessionLocal, engine #!aaaaaaa
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from datetime import datetime

from fastapi.responses import RedirectResponse, HTMLResponse


from schemas import Token, Respuesta
import usuarios.models as models 
import usuarios.schemas as schemas
import usuarios.service as service


models.Base.metadata.create_all(bind=engine)

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 15

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="iniciar_sesion")

templates = Jinja2Templates(directory="../templates/usuarios")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/registrar', response_class=HTMLResponse)
def registrar_usuario(request: Request):
    return templates.TemplateResponse(request=request, name="registrar.html")      

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
    service.registrar_usuario(db=db, usuario=usuario)
    return RedirectResponse(url='/', status_code=status.HTTP_303_SEE_OTHER)


@router.delete('/usuario/{cedula}', response_model=schemas.Usuario)
def borrar_usuario(cedula : str, db: Session = Depends(get_db)): 
    return service.eliminar_usuario(db=db, cedula=cedula)

@router.post('/iniciar_sesion', response_model=Token)
def iniciar_sesion(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)): 
    usuario = service.autenticar_usuario(db, form_data.username, form_data.password)
    if usuario == False: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Credenciales incorrectas', 
            headers={"WWW-Authenticate": "Bearer"}
        )
    tiempo_expiracion = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    nombre_completo = f'{usuario.nombres} {usuario.apellidos}'
    token_acceso = service.crear_token_acceso(
        data={'cedula': usuario.cedula, 
              'nombre_completo': nombre_completo, 
              'tipo_usuario_id': usuario.tipo_id}, 
        expires_delta=tiempo_expiracion
    )
    return Token(usuario=nombre_completo, token_acceso=token_acceso, tipo_token='bearer')