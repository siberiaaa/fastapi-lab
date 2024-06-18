from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from typing import Annotated
from usuarios.router import oauth2_scheme
from usuarios.service import SECRET_KEY, ALGORITHM
from schemas import DataToken

# No sirve :(
def transformar(modelo : object, schema : object):
    print('holaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaas')
    lista_schema = []
    for esto in dir(schema): 
        if '__' not in esto: 
            lista_schema.append(esto)
    lista_modelo = []
    for esto in dir(modelo): 
        if '__' not in esto:
            lista_modelo.append(esto)
 
    for esto in lista_schema: 
        if esto in lista_modelo: 
            print(esto)
            schema[esto] = modelo[esto]

    return schema

# Si sirve (✿◡‿◡)
async def obtener_usuario_actual(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        nombre_completo: str = payload.get("nombre_completo")
        cedula: str = payload.get('cedula')
        tipo_usuario_id: str = payload.get('tipo_usuario_id')
        if nombre_completo is None or cedula is None or tipo_usuario_id is None:
            raise credentials_exception
        token_data = DataToken(
            nombre_completo=nombre_completo, 
            cedula=cedula, 
            tipo_usuario_id=tipo_usuario_id
            )
        return token_data
    except JWTError:
        raise credentials_exception