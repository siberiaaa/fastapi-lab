from sqlalchemy.orm import Session
import estados_caracteristicas.models as models
import estados_caracteristicas.schemas as schemas

def crear_estado_caracteristica(db: Session, estado_caracteristica: schemas.Estado_CaracteristicaCrear):
    db_estado_caracteristica = models.Estado_Caracteristica(
        nombre=estado_caracteristica.nombre, 
        descripcion=estado_caracteristica.descripcion)
    db.add(db_estado_caracteristica)
    db.commit()
    db.refresh(db_estado_caracteristica)
    return db_estado_caracteristica

def listar_estados_caracteristicas(db: Session): 
    return db.query(models.Estado_Caracteristica).all()

def buscar_estado_caracteristica(db: Session, id: int): 
    return db.query(models.Estado_Caracteristica).filter(models.Estado_Caracteristica.id == id).first()

def modificar_estado_caracteristica(db: Session, id: int, estado: schemas.Estado_CaracteristicaCrear): 
    lista = db.query(models.Estado_Caracteristica).all()
    for este in lista: 
        if este.id == id: 
            este.nombre = estado.nombre
            este.descripcion = estado.descripcion
            break
    db.commit()
    return este

def eliminar_estado_caracteristica(db: Session, id: int): 
    estado = db.query(models.Estado_Caracteristica).filter(models.Estado_Caracteristica.id == id).first()
    db.delete(estado)
    db.commit()
    return estado