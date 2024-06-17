from sqlalchemy.orm import Session
import caracteristicas.models as models
import caracteristicas.schemas as schemas

def crear_caracteristica(db: Session, caracteristica: schemas.CaracteristicaCrear):
    db_caracteristica = models.Caracteristica(
        nombre=caracteristica.nombre, 
        explicacion=caracteristica.explicacion, 
        encargo_id=caracteristica.encargo_id, 
        estado_caracteristica_id=caracteristica.estado_caracteristica_id)
    db.add(db_caracteristica)
    db.commit()
    db.refresh(db_caracteristica)
    return db_caracteristica

def listar_caracteristicas(db: Session): 
    return db.query(models.Caracteristica).all()

def buscar_caracteristica(db: Session, id: int): 
    caracteristica = db.query(models.Caracteristica).filter(models.Caracteristica.id == id).first()
    return caracteristica

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