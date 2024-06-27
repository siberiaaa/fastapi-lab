from sqlalchemy.orm import Session
import metodos_envios.models as models
import metodos_envios.schemas as schemas

def crear_metodo_envio(db: Session, metodo_envio: schemas.Metodo_EnvioCrear):
    db_metodo_envio = models.Metodo_Envio(
        nombre=metodo_envio.nombre, 
        descripcion=metodo_envio.descripcion)
    db.add(db_metodo_envio)
    db.commit()
    db.refresh(db_metodo_envio)
    return db_metodo_envio

def listar_metodos_envios(db: Session): 
    return db.query(models.Metodo_Envio).all()