from sqlalchemy.orm import Session
import calificaciones.models as models
import calificaciones.schemas as schemas

def crear_calificacion(db: Session, calificacion: schemas.CalificacionCrear):
    db_calificacion = models.Calificacion(
        titulo=calificacion.titulo, 
        comentario=calificacion.comentario, 
        estrellas=calificacion.estrellas, 
        emoticono=calificacion.emoticono,  
        usuario_cedula=calificacion.usuario_cedula, 
        producto_id=calificacion.producto_id)
    db.add(db_calificacion)
    db.commit()
    db.refresh(db_calificacion)
    return db_calificacion

def listar_calificaciones(db: Session): 
    return db.query(models.Calificacion).all()

def buscar_calificacion(db: Session, id: int): 
    calificacion = db.query(models.Calificacion).filter(models.Calificacion.id == id).first()
    return calificacion

def modificar_calificacion(db: Session, id: int, calificacion: schemas.CalificacionCrear): 
    lista = db.query(models.Calificacion).all()
    for este in lista: 
        if este.id == id: 
            este.titulo = calificacion.titulo
            este.comentario = calificacion.comentario
            este.estrellas = calificacion.estrellas
            este.emoticono = calificacion.emoticono
            este.usuario_cedula = calificacion.usuario_cedula
            este.producto_id = calificacion.producto_id
            break
    db.commit()
    return este

def eliminar_calificacion(db: Session, id: int): 
    calificacion = db.query(models.Calificacion).filter(models.Calificacion.id == id).first()
    db.delete(calificacion)
    db.commit()
    return calificacion