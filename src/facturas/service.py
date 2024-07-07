from sqlalchemy.orm import Session
import facturas.models as models
import facturas.schemas as schemas
from schemas import Respuesta
from datetime import datetime


import productos.models as producto_models
import compras.models as compra_models
import usuarios.models as usuario_models
import cotizaciones.models as cotizacion_models

import metodos_envios.models as envios_models
import metodos_pagos.models as pagos_models


def crear_factura(db: Session, factura: schemas.FacturaCrear):
    db_factura = models.Factura(
        fecha_entrega=factura.fecha_entrega, 
        cotizacion_id=factura.cotizacion_id,  
        metodo_envio_id=factura.metodo_envio_id, 
        metodo_pago_id=factura.metodo_pago_id)
    db.add(db_factura)
    db.commit()
    db.refresh(db_factura)

    factura = schemas.Factura(id=db_factura.id,
                            fecha_entrega=db_factura.fecha_entrega, 
                            cotizacion_id=db_factura.cotizacion_id,  
                            metodo_envio_id=db_factura.metodo_envio_id, 
                            metodo_pago_id=db_factura.metodo_pago_id) 
    return Respuesta[schemas.Factura](ok=True, mensaje='Factura encontrada', data=factura)

def listar_facturas(db: Session): 
    return db.query(models.Factura).all()

def buscar_factura(db: Session, id: int): 
    factura = db.query(models.Factura).filter(models.Factura.id == id).first()
    return factura

def listar_facturas_cotizaciones(db: Session, id: int): 
    facturas = db.query(models.Factura).filter(models.Factura.cotizacion_id == id).all()
    respuesta = Respuesta[list[schemas.Factura]] (
        ok = True, 
        data = facturas, 
        mensaje = 'Se consiguió la factura exitósamente'
    )
    return respuesta

def modificar_factura(db: Session, id: int, factura: schemas.FacturaCrear): 
    lista = db.query(models.Factura).all()
    for este in lista: 
        if este.id == id: 
            este.fecha_entrega = factura.fecha_entrega
            este.cotizacion_id = factura.cotizacion_id
            este.metodo_pago_id = factura.metodo_pago_id
            este.metodo_envio_id = factura.metodo_envio_id
            break
    db.commit()
    return este

def eliminar_factura(db: Session, id: int): 
    factura = db.query(models.Factura).filter(models.Factura.id == id).first()
    db.delete(factura)
    db.commit()
    return factura


def buscar_factura_diccionario(db: Session, id_factura: int): 
    factura = db.query(models.Factura).filter(models.Factura.id == id_factura).first()
    cotizacion = db.query(cotizacion_models.Cotizacion).filter(cotizacion_models.Cotizacion.id == factura.cotizacion_id).first()
    compra = db.query(compra_models.Compra).filter(compra_models.Compra.id == cotizacion.compra_id).first()
    
    envio = db.query(envios_models.Metodo_Envio).filter(envios_models.Metodo_Envio.id == factura.metodo_envio_id).first()
    pago = db.query(pagos_models.Metodo_Pago).filter(pagos_models.Metodo_Pago.id == factura.metodo_pago_id).first()

    factura_diccionario = {}

    factura_diccionario['producto'] = db.query(producto_models.Producto).filter(producto_models.Producto.id == compra.producto_id).first()
    factura_diccionario['compra'] = compra
    factura_diccionario['vendedor'] = db.query(usuario_models.Usuario).filter(usuario_models.Usuario.cedula == factura_diccionario['producto'].usuario_cedula).first()
    factura_diccionario['factura'] = factura
    factura_diccionario['cotizacion'] = cotizacion
    factura_diccionario['pago'] = pago.nombre
    factura_diccionario['envia'] = envio.nombre

    respuesta = Respuesta[dict](ok=True, mensaje='Datos de la factura encontrado', data=factura_diccionario)
    return respuesta


def listar_facturas_cliente(db: Session, cedula: str): 
    #listar todas las compras del cliente
    # lista = db.query(compra_models.Compra).filter(compra_models.Compra.cliente_cedula == cedula).all()
    
    facturas = db.query(models.Factura).all()

    lista_final = []

    for factura in facturas: 
        cotizacion = db.query(cotizacion_models.Cotizacion).filter(cotizacion_models.Cotizacion.id == factura.cotizacion_id).first()
        compra = db.query(compra_models.Compra).filter(compra_models.Compra.id == cotizacion.compra_id).first()
        if compra.cliente_cedula == cedula: 
            final = {}
            envio = db.query(envios_models.Metodo_Envio).filter(envios_models.Metodo_Envio.id == factura.metodo_envio_id).first()
            pago = db.query(pagos_models.Metodo_Pago).filter(pagos_models.Metodo_Pago.id == factura.metodo_pago_id).first()
            final['producto'] = db.query(producto_models.Producto).filter(producto_models.Producto.id == compra.producto_id).first()
            final['compra'] = compra
            final['vendedor'] = db.query(usuario_models.Usuario).filter(usuario_models.Usuario.cedula == final['producto'].usuario_cedula).first()
            final['factura'] = factura
            final['cotizacion'] = cotizacion
            final['pago'] = pago.nombre
            final['envia'] = envio.nombre
            lista_final.append(final)
    print(lista_final)
    
    respuesta = Respuesta[list[dict]](ok=True, mensaje='Lista de las facturas del cliente encontrada', data=lista_final)
    return respuesta


def listar_facturas_artesano(db: Session, cedula: str): 
    lista = db.query(models.Factura).all()
    lista_final = []
    
    for esto in lista: 
      
            cotizacion = db.query(cotizacion_models.Cotizacion).filter(cotizacion_models.Cotizacion.id == esto.cotizacion_id).first()
            compra = db.query(compra_models.Compra).filter(compra_models.Compra.id == cotizacion.compra_id).first()
            producto = db.query(producto_models.Producto).filter(producto_models.Producto.id == compra.producto_id).first()
            usuario = db.query(usuario_models.Usuario).filter(usuario_models.Usuario.cedula == producto.usuario_cedula).first()

            if usuario.cedula == cedula: 
                factura = db.query(models.Factura).filter(models.Factura.cotizacion_id == cotizacion.id).first()
                envio = db.query(envios_models.Metodo_Envio).filter(envios_models.Metodo_Envio.id == factura.metodo_envio_id).first()
                pago = db.query(pagos_models.Metodo_Pago).filter(pagos_models.Metodo_Pago.id == factura.metodo_pago_id).first()

                final = {}
                final['producto'] = producto
                final['compra'] = compra
                final['factura'] = factura
                final['cotizacion'] = cotizacion
                final['pago'] = pago.nombre
                final['envia'] = envio.nombre
                lista_final.append(final)

    
    respuesta = Respuesta[list[dict]](ok=True, mensaje='Lista de las facturas del cliente encontrada', data=lista_final)
    return respuesta