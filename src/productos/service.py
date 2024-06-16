from sqlalchemy.orm import Session
import productos.models as models
import productos.schemas as schemas

def crear_producto(db: Session, producto: schemas.ProductoCrear):
    db_producto = models.Producto(
        nombre=producto.nombre, 
        descripcion=producto.descripcion, 
        altura_cm=producto.altura_cm, 
        anchura_cm=producto.anchura_cm, 
        profundidad_cm=producto.profundidad_cm, 
        imagen=producto.imagen, 
        peso_gramo=producto.peso_gramo, 
        usuario_cedula=producto.usuario_cedula, 
        tipo_producto_id=producto.tipo_producto_id, 
        categoria_id=producto.categoria_id)
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

def listar_tipos_productos(db: Session): 
    return db.query(models.Producto).all()

def buscar_producto(db: Session, id: int): 
    producto = db.query(models.Producto).filter(models.Producto.id == id).first()
    return producto

def modificar_producto(db: Session, id: int, producto: schemas.ProductoCrear): 
    lista = db.query(models.Producto).all()
    for este in lista: 
        if este.id == id: 
            este.nombre = producto.nombre
            este.descripcion = producto.descripcion
            este.altura_cm = producto.altura_cm
            este.anchura_cm = producto.anchura_cm
            este.profundidad_cm = producto.profundidad_cm
            este.imagen = producto.imagen
            este.peso_gramo = producto.peso_gramo
            este.usuario_cedula = producto.usuario_cedula
            este.tipo_producto_id = producto.tipo_producto_id
            este.categoria_id = producto.categoria_id
            break
    db.commit()
    return este

def eliminar_producto(db: Session, id: int): 
    producto = db.query(models.Producto).filter(models.Producto.id == id).first()
    db.delete(producto)
    db.commit()
    return producto