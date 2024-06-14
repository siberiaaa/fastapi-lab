from sqlalchemy.orm import Session
import tipos_usuario.models as models
import tipos_usuario.schemas as schemas

def crear_tipo_usuario(db: Session, tipo_usuario: schemas.Tipo_UsuarioCrear):
    db_tipo_usuario = models.Tipo_Usuario(
        nombre=tipo_usuario.nombre, 
        descripcion=tipo_usuario.descripcion)
    db.add(db_tipo_usuario)
    db.commit()
    db.refresh(db_tipo_usuario)
    return db_tipo_usuario

def listar_tipos_usuarios(db: Session): 
    return db.query(models.Tipo_Usuario).all()

def buscar_tipo_usuario(db: Session, id: int): 
    tipo_usuario = db.query(models.Tipo_Usuario).filter(models.Tipo_Usuario.id == id).first()
    return tipo_usuario