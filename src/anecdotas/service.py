from sqlalchemy.orm import Session
import anecdotas.models as models
import anecdotas.schemas as schemas

def crear_anecdota(db: Session, anecdota: schemas.AnecdotaCrear):
    db_anecdota = models.Anecdota(
        nombre=anecdota.nombre, 
        descripcion=anecdota.descripcion, 
        reseña_id=anecdota.reseña_id)
    db.add(db_anecdota)
    db.commit()
    db.refresh(db_anecdota)
    return db_anecdota

def listar_tipos_anecdotas(db: Session): 
    return db.query(models.Anecdota).all()

def buscar_anecdota(db: Session, id: int): 
    anecdota = db.query(models.Anecdota).filter(models.Anecdota.id == id).first()
    return anecdota

def modificar_anecdota(db: Session, id: int, anecdota: schemas.AnecdotaCrear): 
    lista = db.query(models.Anecdota).all()
    for este in lista: 
        if este.id == id: 
            este.nombre = anecdota.nombre
            este.descripcion = anecdota.descripcion
            este.reseña_id = anecdota.reseña_id
            break
    db.commit()
    return este

def eliminar_anecdota(db: Session, id: int): 
    anecdota = db.query(models.Anecdota).filter(models.Anecdota.id == id).first()
    db.delete(anecdota)
    db.commit()
    return anecdota