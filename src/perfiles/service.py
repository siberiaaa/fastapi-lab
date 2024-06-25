from compras.models import Compra
from tipos_compra.models import Tipo_Compra
from productos.models import Producto
from sqlalchemy.orm import Session

def listar_compras_cliente(db: Session, cedula: str): 
    return db.query(Compra).filter(Compra.cliente_cedula == cedula).all()