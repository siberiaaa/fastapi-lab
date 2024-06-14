from sqlalchemy.orm import Session
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