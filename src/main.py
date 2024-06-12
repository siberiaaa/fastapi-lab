from compra import router as compra


app.include_router(compra.router, prefix='/pages')

#https://fastapi.tiangolo.com/tutorial/bigger-applications/

# prueba