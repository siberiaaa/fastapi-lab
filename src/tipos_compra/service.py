from sqlalchemy.orm import Session
from schemas import Respuesta
import tipos_compra.models as models
import tipos_compra.schemas as schemas

def crear_tipo_compra(db: Session, tipo_compra: schemas.Tipo_CompraCrear):
    db_tipo_compra = models.Tipo_Compra(
        nombre=tipo_compra.nombre, 
        descripcion=tipo_compra.descripcion)
    db.add(db_tipo_compra)
    db.commit()
    db.refresh(db_tipo_compra)
    return db_tipo_compra

def listar_tipos_compras(db: Session): 
    return db.query(models.Tipo_Compra).all()

def get_tipo_compra(db: Session, id: int):
    returned = db.query(models.Tipo_Compra).filter(models.Tipo_Compra.id == id).first()

    if returned == None:
        return Respuesta[schemas.Tipo_Compra](ok=False, mensaje='Tipo de compra no encontrado')

    tipo_compra = schemas.Tipo_Compra(nombre=returned.nombre, descripcion=returned.descripcion, id=returned.id) 
    return Respuesta[schemas.Tipo_Compra](ok=True, mensaje='Tipo de compra no encontrado', data=tipo_compra)