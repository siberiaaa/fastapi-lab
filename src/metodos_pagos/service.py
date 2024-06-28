from sqlalchemy.orm import Session
from schemas import Respuesta

import metodos_pagos.models as models
import metodos_pagos.schemas as schemas

def crear_metodo_pago(db: Session, metodo_pago: schemas.Metodo_PagoCrear):
    db_metodo_pago = models.Metodo_Pago(
        nombre=metodo_pago.nombre, 
        descripcion=metodo_pago.descripcion)
    db.add(db_metodo_pago)
    db.commit()
    db.refresh(db_metodo_pago)
    return db_metodo_pago

def listar_metodos_pagos(db: Session): 
    returned = db.query(models.Metodo_Pago).all()

    pagos = []

    for pag in returned:
        pago = schemas.Metodo_Pago(nombre=pag.nombre, descripcion=pag.descripcion, id=pag.id) 
        pagos.append(pago)

    respuesta = Respuesta[list[schemas.Metodo_Pago]](ok=True, mensaje='Métodos de pago encontrados', data=pagos)
    return respuesta
