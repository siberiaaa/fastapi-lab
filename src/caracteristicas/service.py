from sqlalchemy.orm import Session
from schemas import Respuesta
import caracteristicas.models as models
import caracteristicas.schemas as schemas

import compras.service as compra_service

def crear_caracteristica(db: Session, caracteristica: schemas.CaracteristicaCrear):
     ### Validaciones ###

    #!VALIDACION USUARIO

    #Existe compra
    respuesta_compra = compra_service.get_compra(db=db, id=caracteristica.encargo_id)
    if not respuesta_compra.ok:
        return Respuesta[schemas.Caracteristica](ok=False, mensaje='No existe el id del encargo al que se le desea asignar una característica')
    ### ------------ ###

    db_caracteristica = models.Caracteristica(
        nombre=caracteristica.nombre, 
        explicacion=caracteristica.explicacion, 
        encargo_id=caracteristica.encargo_id, 
        estado_caracteristica_id=1)
    db.add(db_caracteristica)
    db.commit()
    db.refresh(db_caracteristica)

    caracteristica = schemas.Caracteristica(
        id=db_caracteristica.id,
        nombre=db_caracteristica.nombre, 
        explicacion=db_caracteristica.explicacion, 
        encargo_id=db_caracteristica.encargo_id, 
        estado_caracteristica_id=1)
    respuesta = Respuesta[schemas.Caracteristica](ok=True, mensaje='Caracteristica creada', data=caracteristica)
    return respuesta

def aprobar_caracteristica(db: Session, id_caracteristica: int):
    ### Validaciones ###
    #!VALIDACION USUARIO
    
    #Existe caracteristica
    caracteristica_found = db.query(models.Caracteristica).filter(models.Caracteristica.id == id_caracteristica).first()

    if caracteristica_found == None:
        return Respuesta[schemas.Cotizacion](ok=False, mensaje='Característica a aprobar no encontrada')

    ### ------------ ###

    caracteristica_found.estado_caracteristica_id = 2
    db.commit()

    return Respuesta[schemas.Caracteristica](ok=True, mensaje='Característica aprobada exitosamente')

def rechazar_todas_caracteristicas(db: Session, id_encargo: int): 
    returned = db.query(models.Caracteristica).filter(models.Caracteristica.encargo_id == id_encargo).all()

    for caracteristica in returned:
        caracteristica.estado_caracteristica_id = 3

    db.commit()
    return Respuesta[schemas.Caracteristica](ok=True, mensaje='Características rechazadas exitosamente')


def rechazar_caracteristica(db: Session, id_caracteristica: int):
    ### Validaciones ###
    #!VALIDACION USUARIO
    
    #Existe caracteristica
    caracteristica_found = db.query(models.Caracteristica).filter(models.Caracteristica.id == id_caracteristica).first()

    if caracteristica_found == None:
        return Respuesta[schemas.Caracteristica](ok=False, mensaje='Característica a aprobar no encontrada')

    ### ------------ ###

    caracteristica_found.estado_caracteristica_id = 3
    db.commit()

    return Respuesta[schemas.Caracteristica](ok=True, mensaje='Característica rechazada exitosamente')

def get_caracteristicas(db: Session): 
    returned = db.query(models.Caracteristica).all()

    caracteristicas = []

    for cat in returned:
        caracteristica = schemas.Caracteristica(
        id=cat.id,
        nombre=cat.nombre, 
        explicacion=cat.explicacion, 
        encargo_id=cat.encargo_id, 
        estado_caracteristica_id=cat.estado_caracteristica_id)
    
        caracteristicas.append(caracteristica)

    return Respuesta[list[schemas.Caracteristica]](ok=True, mensaje='Características encontradas', data=caracteristicas)

def get_caracteristicas_encargo(db: Session, id_encargo: int): 
    returned = db.query(models.Caracteristica).filter(models.Caracteristica.encargo_id == id_encargo).all()

    caracteristicas = []

    for cat in returned:
        caracteristica = schemas.Caracteristica(
        id=cat.id,
        nombre=cat.nombre, 
        explicacion=cat.explicacion, 
        encargo_id=cat.encargo_id, 
        estado_caracteristica_id=cat.estado_caracteristica_id)
    
        caracteristicas.append(caracteristica)

    return Respuesta[list[schemas.Caracteristica]](ok=True, mensaje='Características del encargo encontradas', data=caracteristicas)

def get_caracteristicas_aprobadas_encargo(db: Session, id_encargo: int): 
    returned = db.query(models.Caracteristica).filter(models.Caracteristica.encargo_id == id_encargo).filter(models.Caracteristica.estado_caracteristica_id == 2).all()

    caracteristicas = []

    for cat in returned:
        caracteristica = schemas.Caracteristica(
        id=cat.id,
        nombre=cat.nombre, 
        explicacion=cat.explicacion, 
        encargo_id=cat.encargo_id, 
        estado_caracteristica_id=cat.estado_caracteristica_id)
    
        caracteristicas.append(caracteristica)

    return Respuesta[list[schemas.Caracteristica]](ok=True, mensaje='Características aprobadas del encargo encontradas', data=caracteristicas)



def get_caracteristica(db: Session, id: int): 
    returned = db.query(models.Caracteristica).filter(models.Caracteristica.id == id).first()

    if returned == None:
        return Respuesta[schemas.Caracteristica](ok=False, mensaje='Característica no encontrada')

    caracteristica = schemas.Caracteristica(id=returned.id,
        nombre=returned.nombre, 
        explicacion=returned.explicacion, 
        encargo_id=returned.encargo_id, 
        estado_caracteristica_id=returned.estado_caracteristica_id) 
    return Respuesta[schemas.Caracteristica](ok=True, mensaje='Característica encontrada', data=caracteristica)


def modificar_caracteristica(db: Session, id: int, caracteristica: schemas.CaracteristicaCrear): 
    lista = db.query(models.Caracteristica).all()
    for este in lista: 
        if este.id == id: 
            este.nombre = caracteristica.nombre
            este.explicacion = caracteristica.explicacion
            este.encargo_id = caracteristica.encargo_id
            este.estado_caracteristica_id = caracteristica.estado_caracteristica_id
            break
    db.commit()
    return este

def eliminar_caracteristica(db: Session, id: int): 
    caracteristica = db.query(models.Caracteristica).filter(models.Caracteristica.id == id).first()
    db.delete(caracteristica)
    db.commit()
    return caracteristica