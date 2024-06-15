from sqlalchemy.orm import Session
import usuarios.models as models
import usuarios.schemas as schemas

# def registrar_usuario(db: Session, usuario: schemas.UsuarioCrear):
#     db_usuario = models.Usuario(
#         cedula=usuario.cedula, 
#         nombres=usuario.nombres, 
#         apellidos=usuario.apellidos, 
#         direccion=usuario.direccion, 
#         nacimiento=usuario.nacimiento, 
#         correo=usuario.correo, 
#         contraseña=usuario.contraseña, 
#         tipo_id=usuario.tipo_id)
#     db.add(db_usuario)
#     db.commit()
#     db.refresh(db_usuario)
#     return db_usuario

# def listar_usuarios(db: Session): 
#     return db.query(models.Usuario).all()

# def buscar_usuario(db: Session, cedula: str): 
#     usuario = db.query(models.Usuario).filter(models.Usuario.cedula == cedula).first()
#     return usuario

