from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from categorias import router as categorias
from estados_compras import router as estados_compras
from estados_cotizacion import router as estados_cotizacion
from metodos_envios import router as metodos_envios
from tipos_compra import router as tipos_compra
from metodos_pagos import router as metodos_pagos
from estados_caracteristicas import router as estados_caracteristicas
from tipos_usuario import router as tipos_usuario
from tipos_producto import router as tipos_productos
from usuarios import router as usuarios
from productos import router as productos
from calificaciones import router as calificaciones
from reseñas import router as reseñas
from anecdotas import router as anecdotas
from compras import router as compras
from caracteristicas import router as caracteristicas
from cotizaciones import router as cotizaciones
from facturas import router as facturas

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "27A0D7C4CCCE76E6BE39225B7EEE8BD0EF890DE82D49E459F4C405C583080AB0"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="iniciar_sesion")

app.include_router(categorias.router, prefix='/categorias')
app.include_router(estados_compras.router, prefix='/estados_compras')
app.include_router(estados_cotizacion.router, prefix='/estados_cotizacion')
app.include_router(metodos_envios.router, prefix='/metodos_envios')
app.include_router(tipos_compra.router, prefix='/tipos_compras')
app.include_router(metodos_pagos.router, prefix='/metodos_pagos')
app.include_router(estados_caracteristicas.router, prefix='/estados_caracteristicas')
app.include_router(tipos_usuario.router, prefix='/tipos_usuarios')
app.include_router(tipos_productos.router, prefix='/tipos_productos')
app.include_router(usuarios.router)
app.include_router(productos.router, prefix='/productos')
app.include_router(calificaciones.router, prefix='/calificaciones')
app.include_router(reseñas.router, prefix='/reseñas')
app.include_router(anecdotas.router, prefix='/anecdotas')
app.include_router(compras.router, prefix='/compras')
app.include_router(caracteristicas.router, prefix='/caracteristicas')
app.include_router(cotizaciones.router, prefix='/cotizaciones')
app.include_router(facturas.router, prefix='/facturas')


@app.get('/')
def home():
    return {"message": "Hello world"}

#https://fastapi.tiangolo.com/tutorial/bigger-applications/
#https://github.com/zhanymkanov/fastapi-best-practices#1-project-structure-consistent--predictable

# prueba