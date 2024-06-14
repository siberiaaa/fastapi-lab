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