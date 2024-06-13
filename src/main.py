from fastapi import FastAPI
from categorias import router as categorias

app = FastAPI()

app.include_router(categorias.router, prefix='/categorias')

@app.get('/')
def home():
    return {"message":"Hello world"}

#https://fastapi.tiangolo.com/tutorial/bigger-applications/
#https://github.com/zhanymkanov/fastapi-best-practices#1-project-structure-consistent--predictable

# prueba