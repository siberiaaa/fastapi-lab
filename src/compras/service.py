from sqlalchemy.orm import Session
import compras.models as models
import compras.schemas as schemas

def crear_compra(db: Session, compra: schemas.CompraCrear):
    db_compra = models.Compra(
        cantidad=compra.cantidad, 
        fecha=compra.fecha, 
        cliente_cedula=compra.cliente_cedula, 
        producto_id=compra.producto_id, 
        tipo_compra_id=compra.tipo_compra_id, 
        estado_compra_id=compra.estado_compra_id)
    db.add(db_compra)
    db.commit()
    db.refresh(db_compra)
    return db_compra

def listar_compras(db: Session): 
    return db.query(models.Compra).all()

def buscar_compra(db: Session, id: int): 
    compra = db.query(models.Compra).filter(models.Compra.id == id).first()
    return compra

def modificar_compra(db: Session, id: int, compra: schemas.CompraCrear): 
    lista = db.query(models.Compra).all()
    for este in lista: 
        if este.id == id: 
            este.cantidad = compra.cantidad
            este.fecha = compra.fecha
            este.cliente_cedula = compra.cliente_cedula
            este.producto_id = compra.producto_id
            este.tipo_compra_id = compra.tipo_compra_id
            este.estado_compra_id = compra.estado_compra_id
            break
    db.commit()
    return este

def eliminar_compra(db: Session, id: int): 
    compra = db.query(models.Compra).filter(models.Compra.id == id).first()
    db.delete(compra)
    db.commit()
    return compra