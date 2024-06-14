from sqlalchemy.orm import Session
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