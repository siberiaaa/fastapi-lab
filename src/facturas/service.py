from sqlalchemy.orm import Session
import facturas.models as models
import facturas.schemas as schemas
from schemas import Respuesta

def crear_factura(db: Session, factura: schemas.FacturaCrear):
    db_factura = models.Factura(
        fecha_entrega=factura.fecha_entrega, 
        cotizacion_id=factura.cotizacion_id,  
        metodo_envio_id=factura.metodo_envio_id, 
        metodo_pago_id=factura.metodo_pago_id)
    db.add(db_factura)
    db.commit()
    db.refresh(db_factura)
    return db_factura

def listar_facturas(db: Session): 
    return db.query(models.Factura).all()

def buscar_factura(db: Session, id: int): 
    factura = db.query(models.Factura).filter(models.Factura.id == id).first()
    return factura

def listar_facturas_cotizaciones(db: Session, id: int): 
    facturas = db.query(models.Factura).filter(models.Factura.cotizacion_id == id).all()
    respuesta = Respuesta[list[schemas.Factura]] (
        ok = True, 
        data = facturas, 
        mensaje = 'Se consiguió la factura exitósamente'
    )
    return respuesta

def modificar_factura(db: Session, id: int, factura: schemas.FacturaCrear): 
    lista = db.query(models.Factura).all()
    for este in lista: 
        if este.id == id: 
            este.fecha_entrega = factura.fecha_entrega
            este.cotizacion_id = factura.cotizacion_id
            este.metodo_pago_id = factura.metodo_pago_id
            este.metodo_envio_id = factura.metodo_envio_id
            break
    db.commit()
    return este

def eliminar_factura(db: Session, id: int): 
    factura = db.query(models.Factura).filter(models.Factura.id == id).first()
    db.delete(factura)
    db.commit()
    return factura