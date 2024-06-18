from sqlalchemy.orm import Session
from schemas import Respuesta
import cotizaciones.models as models
import cotizaciones.schemas as schemas

import compras.service as compra_service
#import estados_cotizacion.service as estado_cotizacion_service

def crear_cotizacion(db: Session, cotizacion: schemas.CotizacionCrear):
     ### Validaciones ###

    #!VALIDACION USUARIO

    #Existe compra
    respuesta_compra = compra_service.get_compra(db=db, id=cotizacion.compra_id)
    if not respuesta_compra.ok:
        return Respuesta[schemas.Cotizacion](ok=False, mensaje='No existe el id de la compra del que intenta realizar la cotización')

    #Compra tiene estado aprobado
    if respuesta_compra.data.estado_compra_id != 2:
        return Respuesta[schemas.Cotizacion](ok=False, mensaje='No se puede crear cotización a una compra que no haya sido previamente aprobada')

    # #Existe estado de cotización
    # respuesta_estado_cotizacion = estado_cotizacion_service.get_estado_cotizacion(db=db, id=cotizacion.estado_cotizacion_id)
    # if not respuesta_estado_cotizacion.ok: Respuesta[schemas.Compra](ok=False, mensaje='No existe el estado de compra registrado con el cual se intenta realizar la compra')

    ### ------------ ###


    db_cotizacion = models.Cotizacion(
        precio=cotizacion.precio, 
        compra_id=cotizacion.compra_id,  
        estado_cotizacion_id=1)
    
    db.add(db_cotizacion)
    db.commit()
    db.refresh(db_cotizacion)

    compra = schemas.Compra(id=db_cotizacion.id, 
                            precio=db_cotizacion.precio, 
                            estado_cotizacion_id=db_cotizacion.estado_cotizacion_id) 
    respuesta = Respuesta[schemas.Cotizacion](ok=True, mensaje='Cotización realizada', data=compra)
    return respuesta

def aprobar_cotizacion(db: Session, id_cotizacion: int):
    ### Validaciones ###

    # El usuario loggeado que ejecuta esta petición sea el cliente que solicitó la compra del producto (#!VALIDACION USUARIO)
    #
    #

    #Existe cotización
    cotizacion_found = db.query(models.Cotizacion).filter(models.Cotizacion.id == id_cotizacion).first()

    if cotizacion_found == None:
        return Respuesta[schemas.Cotizacion](ok=False, mensaje='Cotización a aprobar no encontrada')
     
    #Verificar que todas las características tengan estado aprobado o rechazado si la compra es de tipo encargo 
    respuesta_compra = compra_service.get_compra(db=db, id=cotizacion_found.compra_id)
    if not respuesta_compra.ok:
        return Respuesta[schemas.Cotizacion](ok=False, mensaje='No existe el id de la compra de la cotización que se intenta aprobar')

    if respuesta_compra.data.tipo_compra_id == 2:
        pass #! Hacer 
    ### ------------ ###

    cotizacion_found.estado_cotizacion = 2
    db.commit()

    return Respuesta[schemas.Cotizacion](ok=True, mensaje='Cotización aprobada exitosamente')

def rechazar_cotizacion(db: Session, id_cotizacion: int):
    ### Validaciones ###

    # El usuario loggeado que ejecuta esta petición sea el cliente que solicitó la compra del producto (#!VALIDACION USUARIO)
    #
    #

    #Existe cotización
    cotizacion_found = db.query(models.Cotizacion).filter(models.Cotizacion.id == id_cotizacion).first()

    if cotizacion_found == None:
        return Respuesta[schemas.Cotizacion](ok=False, mensaje='Cotización a aprobar no encontrada')
     
    ### ------------ ###

    cotizacion_found.estado_cotizacion = 3
    db.commit()

    return Respuesta[schemas.Cotizacion](ok=True, mensaje='Cotización rechazada exitosamente')

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