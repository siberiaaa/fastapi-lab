from sqlalchemy.orm import Session
import cotizaciones.models as models
import cotizaciones.schemas as schemas

def crear_cotizacion(db: Session, cotizacion: schemas.CotizacionCrear):
    db_cotizacion = models.Cotizacion(
        precio=cotizacion.precio, 
        compra_id=cotizacion.compra_id,  
        estado_cotizacion_id=cotizacion.estado_cotizacion_id)
    db.add(db_cotizacion)
    db.commit()
    db.refresh(db_cotizacion)
    return db_cotizacion

def listar_cotizaciones(db: Session): 
    return db.query(models.Cotizacion).all()

def buscar_cotizacion(db: Session, id: int): 
    cotizacion = db.query(models.Cotizacion).filter(models.Cotizacion.id == id).first()
    return cotizacion

def modificar_cotizacion(db: Session, id: int, cotizacion: schemas.CotizacionCrear): 
    lista = db.query(models.Cotizacion).all()
    for este in lista: 
        if este.id == id: 
            este.precio = cotizacion.precio
            este.compra_id = cotizacion.compra_id
            este.estado_cotizacion_id = cotizacion.estado_cotizacion_id
            break
    db.commit()
    return este

def eliminar_cotizacion(db: Session, id: int): 
    cotizacion = db.query(models.Cotizacion).filter(models.Cotizacion.id == id).first()
    db.delete(cotizacion)
    db.commit()
    return cotizacion