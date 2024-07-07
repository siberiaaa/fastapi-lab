from fastapi import APIRouter, Depends, Form, status, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import Annotated
from database import SessionLocal, engine
from datetime import datetime
from reportes import service
from productos import schemas
from exceptions import No_Artesano_Exception

router = APIRouter()

from usuarios.service import AuthHandler
auth_handler = AuthHandler()

templates = Jinja2Templates(directory="../templates")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/reportes')
def mostrar_reportes(request: Request, inicio: datetime, 
                     final: datetime, db = Depends(get_db), 
                     info = Depends(auth_handler.auth_wrapper)): 
    if info['tipo_usuario_id'] != 1: 
        raise No_Artesano_Exception()
    lista = service.reportes_fecha_vendiddos(db=db, inicio=inicio, final=final, cedula=info['cedula'])
    lista_imagenes = []
    for esto in lista: 
        real = bytes(esto.imagen).decode()
        lista_imagenes.append(real)
    return templates.TemplateResponse(request=request, name='/homes/artesanos.html', context={
        "info": info, 
        'lista': lista, 
        'imagenes': lista_imagenes
    })