from sqlalchemy.orm import Session
import tipos_producto.models as models
import tipos_producto.schemas as schemas

def crear_tipo_producto(db: Session, tipo_producto: schemas.Tipo_ProductoCrear):
    db_tipo_producto = models.Tipo_Producto(
        nombre=tipo_producto.nombre, 
        descripcion=tipo_producto.descripcion, 
        funcionalidad=tipo_producto.funcionalidad)
    db.add(db_tipo_producto)
    db.commit()
    db.refresh(db_tipo_producto)
    return db_tipo_producto

def listar_tipos_productos(db: Session): 
    return db.query(models.Tipo_Producto).all()

def buscar_tipo_producto(db: Session, id: int): 
    tipo_producto = db.query(models.Tipo_Producto).filter(models.Tipo_Producto.id == id).first()
    return tipo_producto

def modificar_tipo_producto(db: Session, id: int, tipo_producto: schemas.Tipo_ProductoCrear): 
    lista = db.query(models.Tipo_Producto).all()
    for este in lista: 
        if este.id == id: 
            este.nombre = tipo_producto.nombre
            este.descripcion = tipo_producto.descripcion
            este.funcionalidad = tipo_producto.funcionalidad
            break
    db.commit()
    return este

def eliminar_tipo_producto(db: Session, id: int): 
    tipo_producto = db.query(models.Tipo_Producto).filter(models.Tipo_Producto.id == id).first()
    db.delete(tipo_producto)
    db.commit()
    return tipo_producto