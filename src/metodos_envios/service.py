from sqlalchemy.orm import Session
from schemas import Respuesta

import metodos_envios.models as models
import metodos_envios.schemas as schemas

def crear_metodo_envio(db: Session, metodo_envio: schemas.Metodo_EnvioCrear):
    db_metodo_envio = models.Metodo_Envio(
        nombre=metodo_envio.nombre, 
        descripcion=metodo_envio.descripcion)
    db.add(db_metodo_envio)
    db.commit()
    db.refresh(db_metodo_envio)
    return db_metodo_envio

def listar_metodos_envios(db: Session): 
    returned = db.query(models.Metodo_Envio).all()

    envios = []

    for env in returned:
        envio = schemas.Metodo_Envio(nombre=env.nombre, descripcion=env.descripcion, id=env.id) 
        envios.append(envio)

    respuesta = Respuesta[list[schemas.Metodo_Envio]](ok=True, mensaje='Métodos de envío encontrados', data=envios)
    return respuesta
