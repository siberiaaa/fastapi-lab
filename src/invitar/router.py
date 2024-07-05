from typing import List
from fastapi.templating import Jinja2Templates
from fastapi import BackgroundTasks, APIRouter, File, Form, UploadFile, Depends, Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel
from usuarios.service import AuthHandler
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import cm
from reportlab.pdfgen.canvas import Canvas


# https://www.geeksforgeeks.org/sending-email-using-fastapi-framework-in-python/
# https://www.hostinger.es/tutoriales/como-usar-el-servidor-smtp-gmail-gratuito/

auth_handler = AuthHandler()

router = APIRouter()

templates = Jinja2Templates(directory="../templates")

class EmailSchema(BaseModel):
    email: List[EmailStr]

conf = ConnectionConfig(
    MAIL_USERNAME = "empresamariamoonlit72@gmail.com",
    MAIL_PASSWORD = "qmoz cnct ebek jnkn",
    MAIL_FROM = "empresamariamoonlit72@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME="Artesanal",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

router = APIRouter()



@router.post('/linear')
def lineas(request: Request, lineas : list[str] = Form(...)): 
    return {'lineas': lineas}

# @router.get('/descargar_factura')
# def lineas(): 
#     canvas = Canvas(f"factura.pdf", pagesize=LETTER)

#     canvas.drawString(2 * cm, 8 * cm, "Hello, Real Python!")

#     canvas.save()
#     return {'lineas': 'hola'}

@router.get('/invitar')
def invitar(request: Request, info=Depends(auth_handler.auth_wrapper)): 
    return templates.TemplateResponse('/invitar/invitar.html', {
        'request': request, 'info': info
    })

@router.post("/mandar_correo")
async def mandar_simple(
        request: Request, 
        original: EmailStr = Form(...), 
        info=Depends(auth_handler.auth_wrapper)):
    emailFinal = EmailSchema(
        email= [
            original
        ]
    )
    html = f"""
    <h1>Invitación cordial a Artesanal</h1>
    <p>
        Hoy has sido cordialmente invitado a nuestra aplicación 'Artesanal' por {info['nombre_completo']} <br>
        Que tenga un maravilloso día en nuestra aplicación https://anapaulasiberialaboratoriofastapigracoso.onrender.com/
    </p>
    """
    message = MessageSchema(
        subject="Invitación cordial a Artesanal",
        recipients=emailFinal.model_dump().get('email'),
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    print("Fast mail: ", fm)
    await fm.send_message(message)
    # return JSONResponse(status_code=200, content={"message": "email has been sent"})
    return templates.TemplateResponse('/usuarios/principal.html', {
        'request': request, 'info': info})

@router.post("/emailbackground")
async def send_in_background(
    background_tasks: BackgroundTasks,
    email: EmailSchema
    ) -> JSONResponse:

    message = MessageSchema(
        subject="Saludos desde artesanal",
        recipients=email.model_dump().get('email'),
        body="Hola queridaaaaaaaaa :3",
        subtype=MessageType.plain)

    fm = FastMail(conf)

    background_tasks.add_task(fm.send_message,message)

    return JSONResponse(status_code=200, content={"message": "email has been sent"})

# @router.post("/file")
# async def send_file(
#     background_tasks: BackgroundTasks,
#     file: UploadFile = File(...),
#     email: EmailStr = Form(...)
#     ) -> JSONResponse:

#     message = MessageSchema(
#             subject="Fastapi mail module",
#             recipients=[email],
#             body="Simple background task",
#             subtype=MessageType.html,
#             attachments=[file])

#     fm = FastMail(conf)

#     background_tasks.add_task(fm.send_message,message)

#     return JSONResponse(status_code=200, content={"message": "email has been sent"})
