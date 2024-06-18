from sqlalchemy.orm import Session
from schemas import Respuesta
import estados_cotizacion.models as models
import estados_cotizacion.schemas as schemas

def crear_estado_cotizacion(db: Session, estado_cotizacion: schemas.Estado_CotizacionCrear):
    db_estado_cotizacion = models.Estado_Cotizacion(
        nombre=estado_cotizacion.nombre, 
        descripcion=estado_cotizacion.descripcion)
    db.add(db_estado_cotizacion)
    db.commit()
    db.refresh(db_estado_cotizacion)
    return db_estado_cotizacion

def get_estado_cotizacion(db: Session, id: int):
    returned = db.query(models.Estado_Cotizacion).filter(models.Estado_Cotizacion.id == id).first()

    if returned == None:
        return Respuesta[schemas.Estado_Cotizacion](ok=False, mensaje='Estado de cotización no encontrado')

    estado_cotizacion = schemas.Estado_Cotizacion(nombre=returned.nombre, descripcion=returned.descripcion, id=returned.id) 
    return Respuesta[schemas.Estado_Cotizacion](ok=True, mensaje='Estado de cotización encontrado', data=estado_cotizacion)