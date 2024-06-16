from sqlalchemy.orm import Session
import reseñas.models as models
import reseñas.schemas as schemas

def crear_reseña(db: Session, reseña: schemas.ReseñaCrear):
    db_reseña = models.Reseña(
        invencion=reseña.invencion, 
        inventor=reseña.inventor, 
        años_produccion=reseña.años_produccion, 
        producto_id=reseña.producto_id)
    db.add(db_reseña)
    db.commit()
    db.refresh(db_reseña)
    return db_reseña

def listar_tipos_reseñas(db: Session): 
    return db.query(models.Reseña).all()

def buscar_reseña(db: Session, id: int): 
    reseña = db.query(models.Reseña).filter(models.Reseña.id == id).first()
    return reseña

def modificar_reseña(db: Session, id: int, reseña: schemas.ReseñaCrear): 
    lista = db.query(models.Reseña).all()
    for este in lista: 
        if este.id == id: 
            este.invencion = reseña.invencion
            este.inventor = reseña.inventor
            este.años_produccion = reseña.años_produccion
            este.producto_id = reseña.producto_id
            break
    db.commit()
    return este

def eliminar_reseña(db: Session, id: int): 
    reseña = db.query(models.Reseña).filter(models.Reseña.id == id).first()
    db.delete(reseña)
    db.commit()
    return reseña