from sqlalchemy.orm import Session
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