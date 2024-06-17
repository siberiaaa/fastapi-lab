from sqlalchemy.orm import Session
from schemas import Respuesta
import productos.models as models
import productos.schemas as schemas

def create_producto(db: Session, producto: schemas.ProductoCrear):
    db_producto = models.Producto(nombre=producto.nombre, 
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

    producto = schemas.Producto(
        id=db_producto.id,
        nombre=db_producto.nombre, 
        descripcion=db_producto.descripcion, 
        altura_cm=db_producto.altura_cm, 
        anchura_cm=db_producto.anchura_cm, 
        altura_profundidad_cm=db_producto.profundidad_cm, 
        imagen=db_producto.imagen, 
        peso_gramo=db_producto.peso_gramo, 
        usuario_cedula=db_producto.usuario_cedula, 
        tipo_producto_id=db_producto.tipo_producto_id, 
        categoria_id=db_producto.categoria_id, 
        ) 
    
    respuesta = Respuesta[schemas.Producto](ok=True, mensaje='Producto creado', data=producto)
    return respuesta

def get_productos(db: Session): 
    returned = db.query(models.Producto).all()

    respuesta = Respuesta[list[schemas.Producto]](ok=True, mensaje='Productos encontrados', data=returned)
    return respuesta

def get_productos_por_artesano(db: Session, cedula_artesano: int): 
    returned = db.query(models.Producto).filter(models.Producto.usuario_cedula == cedula_artesano).all()

    respuesta = Respuesta[list[schemas.Producto]](ok=True, mensaje='Productos encontrados', data=returned)
    return respuesta

def get_producto(db: Session, id: int): 
    returned = db.query(models.Producto).filter(models.Producto.id == id).first()
    
    if returned == None:
        return Respuesta[schemas.Producto](ok=False, mensaje='Producto no encontrado')

    producto = schemas.Producto(
        id=returned.id,
        nombre=returned.nombre, 
        descripcion=returned.descripcion, 
        altura_cm=returned.altura_cm, 
        anchura_cm=returned.anchura_cm, 
        altura_profundidad_cm=returned.profundidad_cm, 
        imagen=returned.imagen, 
        peso_gramo=returned.peso_gramo, 
        usuario_cedula=returned.usuario_cedula, 
        tipo_producto_id=returned.tipo_producto_id, 
        categoria_id=returned.categoria_id, 
        ) 
    
    return Respuesta[schemas.Producto](ok=True, mensaje='Producto encontrado', data=producto)

def update_producto(db: Session, id: int, producto: schemas.ProductoCrear): 
    productoFound = db.query(models.Producto).filter(models.Producto.id == id).first()

    if productoFound == None:
        return Respuesta[schemas.Producto](ok=False, mensaje='Producto a actualizar no encontrado')

    productoFound.nombre = producto.nombre
    productoFound.descripcion = producto.descripcion
    productoFound.altura_cm = producto.altura_cm
    productoFound.anchura_cm = producto.anchura_cm
    productoFound.profundidad_cm = producto.profundidad_cm
    productoFound.imagen = producto.imagen
    productoFound.peso_gramo = producto.peso_gramo
    productoFound.usuario_cedula = producto.usuario_cedula
    productoFound.tipo_producto_id = producto.tipo_producto_id
    productoFound.categoria_id = producto.categoria_id
    db.commit()

    returned = db.query(models.Producto).filter(models.Producto.id == id).first()

    producto = schemas.Producto(
        id=returned.id,
        nombre=returned.nombre, 
        descripcion=returned.descripcion, 
        altura_cm=returned.altura_cm, 
        anchura_cm=returned.anchura_cm, 
        altura_profundidad_cm=returned.profundidad_cm, 
        imagen=returned.imagen, 
        peso_gramo=returned.peso_gramo, 
        usuario_cedula=returned.usuario_cedula, 
        tipo_producto_id=returned.tipo_producto_id, 
        categoria_id=returned.categoria_id, 
        ) 

    respuesta = Respuesta[schemas.Producto](ok=True, mensaje='Producto actualizado', data=producto)
    return respuesta

def delete_producto(db: Session, id: int): 
    productoFound = db.query(models.Producto).filter(models.Producto.id == id).first()

    if productoFound == None:
        return Respuesta[schemas.Producto](ok=False, mensaje='Producto a eliminar no encontrado')

    db.query(models.Producto).filter(models.Producto.id == id).delete()
    db.commit()
    
    return Respuesta[schemas.Producto](ok=True, mensaje='Producto eliminado')