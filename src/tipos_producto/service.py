from sqlalchemy.orm import Session
from schemas import Respuesta
import tipos_producto.models as models
import tipos_producto.schemas as schemas
import productos.models as producto_models

def create_tipo_producto(db: Session, tipo_producto: schemas.Tipo_ProductoCrear):
    db_tipo_producto = models.Tipo_Producto(nombre=tipo_producto.nombre, descripcion=tipo_producto.descripcion, funcionalidad=tipo_producto.funcionalidad)
    db.add(db_tipo_producto)
    db.commit()
    db.refresh(db_tipo_producto)

    tipo_producto = schemas.Tipo_Producto(nombre=db_tipo_producto.nombre, descripcion=db_tipo_producto.descripcion, funcionalidad=db_tipo_producto.funcionalidad, id=db_tipo_producto.id) 
    respuesta = Respuesta[schemas.Tipo_Producto](ok=True, mensaje='Tipo de producto creado', data=tipo_producto)
    return respuesta

def get_tipo_producto(db: Session, id: int): 
    returned = db.query(models.Tipo_Producto).filter(models.Tipo_Producto.id == id).first()
    
    if returned == None:
        return Respuesta[schemas.Tipo_Producto](ok=False, mensaje='Tipo de producto no encontrado')

    tipo_producto = schemas.Tipo_Producto(nombre=returned.nombre, descripcion=returned.descripcion,  funcionalidad=returned.funcionalidad, id=returned.id) 
    return Respuesta[schemas.Tipo_Producto](ok=True, mensaje='Tipo de producto encontrado', data=tipo_producto)

def get_tipos_producto(db: Session): 
    returned = db.query(models.Tipo_Producto).all()

    tipos = []

    for tipo in returned:
        tip = schemas.Tipo_Producto(nombre=tipo.nombre, descripcion=tipo.descripcion,  funcionalidad=tipo.funcionalidad, id=tipo.id)
        tipos.append(tip)

    respuesta = Respuesta[list[schemas.Tipo_Producto]](ok=True, mensaje='Tipos de producto encontrados', data=tipos)
    return respuesta


def update_tipo_producto(db: Session, id: int, tipo_producto: schemas.Tipo_ProductoCrear): 
    tipo_productoFound = db.query(models.Tipo_Producto).filter(models.Tipo_Producto.id == id).first()

    if tipo_productoFound == None:
        return Respuesta[schemas.Tipo_Producto](ok=False, mensaje='Tipo de producto a actualizar no encontrado')

    tipo_productoFound.nombre = tipo_producto.nombre
    tipo_productoFound.descripcion = tipo_producto.descripcion
    tipo_productoFound.funcionalidad = tipo_producto.funcionalidad
    db.commit()

    returned = db.query(models.Tipo_Producto).filter(models.Tipo_Producto.id == id).first()

    tipo_producto = schemas.Tipo_Producto(nombre=returned.nombre, descripcion=returned.descripcion, funcionalidad=returned.funcionalidad, id=returned.id) 
    respuesta = Respuesta[schemas.Tipo_Producto](ok=True, mensaje='Tipo de producto actualizado', data=tipo_producto)
    return respuesta

def delete_tipo_producto(db: Session, id: int): 
    tipo_productoFound = db.query(models.Tipo_Producto).filter(models.Tipo_Producto.id == id).first()

    if tipo_productoFound == None:
        return Respuesta[schemas.Tipo_Producto](ok=False, mensaje='Tipo de producto a eliminar no encontrado')

     #Validamos que no exista algún producto registrado con esta categoría porque sino nao se puede eliminar la cat
    productos = db.query(producto_models.Producto).filter(producto_models.Producto.tipo_producto_id == id).first()

    if productos:
        return Respuesta[schemas.Categoria](ok=False, mensaje='No se puede eliminar una categoría que esté siendo usada por un producto.')
    


    db.query(models.Tipo_Producto).filter(models.Tipo_Producto.id == id).delete()
    db.commit()

    return Respuesta[schemas.Tipo_Producto](ok=True, mensaje='Tipo de producto eliminado')