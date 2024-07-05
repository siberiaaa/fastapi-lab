from fastapi import FastAPI, Response, Depends
from fpdf import FPDF
# from fpdf.enums import XPos, YPos
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, UploadFile, Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel
from usuarios.service import AuthHandler
from database import SessionLocal, engine
from sqlalchemy.orm import Session

import facturas.service as factura_service

auth_handler = AuthHandler()

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

templates = Jinja2Templates(directory="../templates")

def create_PDF(text : list[str]):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('helvetica', 'B', 12)
    for esto in text: 
        pdf.cell(0, 10, esto, 0, 1)
    return pdf.output(dest='S').encode('latin-1')

    
@router.get('/descargar_factura/{id_factura}')
def get_pdf(id_factura: int, info=Depends(auth_handler.auth_wrapper), db: Session = Depends(get_db)):
    factura_infooo = factura_service.buscar_factura_diccionario(db=db, id_factura=id_factura)
    
    factura_info = factura_infooo.data
    factura_info = [
        f"TU FACTURA", 
        f"Factura id: {factura_info['factura'].id}", 
        f"Nombre: {factura_info['producto'].nombre}", 
        f"Cantidad: {factura_info['compra'].cantidad }", 
        f"Precio: { factura_info['cotizacion'].precio }", 
        f"Precio total: { factura_info['cotizacion'].precio * factura_info['compra'].cantidad}", 
        f"Fecha entrega: { factura_info['factura'].fecha_entrega }", 
        f"Método de pago: { factura_info['pago'] }", 
        f"Método de envío: { factura_info['envia'] }"
    ]

    out = create_PDF(factura_info)
    headers = {'Content-Disposition': f'inline; filename="factura-{id_factura}.pdf"'}
    return Response(bytes(out), headers=headers, media_type='application/pdf')