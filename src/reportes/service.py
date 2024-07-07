from datetime import datetime
from facturas import models
from cotizaciones import models as cotizaciones
from compras import models as compras
from productos import models as productos
from sqlalchemy.orm import Session
from collections import Counter

def reportes_fecha_vendiddos(db: Session, inicio: datetime, final: datetime, cedula: str): 
    facturas = db.query(models.Factura).all()
    lista : list[productos.Producto] = []
    lista_nombre = []
    # lista_compras : list[compras.Compra] = []
    for esto in facturas: 
        cotizacion = db.query(cotizaciones.Cotizacion).filter(cotizaciones.Cotizacion.id == esto.cotizacion_id).first()
        compra = db.query(compras.Compra).filter(compras.Compra.id == cotizacion.compra_id).first()
        if compra.fecha >= inicio and compra.fecha <= final: 
            producto = db.query(productos.Producto).filter(productos.Producto.id == compra.producto_id).first()
            if producto.usuario_cedula == cedula: 
                # lista_compras.append(compra)
                buscar(lista_nombre, producto)
    lista_nombre.sort(key=lambda x: x['veces'], reverse=True)
    for esto in lista_nombre: 
        producto = db.query(productos.Producto).filter(productos.Producto.id == esto['id']).first()
        lista.append(producto)
    # lista_compras.sort(key=obtener_)
    # for esto in lista_compras: 
    #     producto = db.query(productos.Producto).filter(productos.Producto.id == compra.producto_id).first()
    #     lista.append(producto)
    return lista

def buscar(lista : list, producto : productos.Producto): 
    for esto in lista: 
        if esto['id'] == producto.id: 
            esto['veces'] += 1
            return
    esto = {
        'id': producto.id, 
        'producto': producto, 
        'veces': 1
    }
    lista.append(esto)

def obtener(e : compras.Compra):
    return e.producto_id