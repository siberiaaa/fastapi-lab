from datetime import datetime, timedelta, timezone
from typing import Annotated, Union
from fastapi import Depends, FastAPI, HTTPException, status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel
from datetime import datetime
import uvicorn

# To get a string like this run
# openssl rand -hex 32

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "27A0D7C4CCCE76E6BE39225B7EEE8BD0EF890DE82D49E459F4C405C583080AB0"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = {
#    "johndoe": {
#     "username": "johndoe",
#     "email": "johndoe@example.com",
#     "hashed_password": "secret",
#     "full_name": "John Doe",
#     "disabled": False
#    },
#    "alice": {
#     "username": "alice",
#     "email": "alice@example.com",
#     "hashed_password": "secret2",
#     "full_name": "Alice Wonderson",
#     "disabled": True
#    }
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class UserRegister(BaseModel):
    username: str
    password: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None

class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None

#to encode jwt token
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def fake_decode_token(token):
    return User(username=token + "dummydecoded", email="john@example.com", full_name="John Doe")

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

#from pass to hash
def get_password_hash(password):
    return pwd_context.hash(password)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    credentials_exception = HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username) #como si fuera a labase de datos
    if user is None:
        raise credentials_exception
    return user #

#verify pass with hashed pass
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def autheticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    #hashed_password = get_password_hash(user.hashed_password)
    if not verify_password(password, user.hashed_password):
        return False
    return user


@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user

@app.post("/signup")
async def sign_up(userRegister: UserRegister):
    hashed_pass = get_password_hash(userRegister.password)
    fake_users_db[userRegister.username] = {
    "username": userRegister.username,
    "email": userRegister.email,
    "hashed_password": hashed_pass,
    "full_name": userRegister.full_name,
    "disabled": userRegister.disabled}

    return userRegister

@app.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = autheticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token= access_token, token_type= "bearer")

# ---------------------------------------------------------------------------

eventos_list = []

class Evento(BaseModel):
    id: int
    titulo: str 
    descripcion: str
    fecha_hora: datetime
    notas_evento: list[str] | None = []
    fue_realizado: bool | None = False

@app.post('/eventos')
async def create_evento(evento: Evento, token: Annotated[str, Depends(oauth2_scheme)]):

    exist = any(e for e in eventos_list if e.id == evento.id)
    if exist:
            raise HTTPException(status_code=404, detail="Ya existe un evento con este id")
    
    eventos_list.append(evento)
    return evento

@app.get('/eventos', response_model=list[Evento])
async def read_eventos(token: Annotated[str, Depends(oauth2_scheme)]) -> list[Evento]:
    return eventos_list

@app.get('/eventos/{id}')
async def read_evento(id:int, token: Annotated[str, Depends(oauth2_scheme)]):
    for evento in eventos_list:
        if evento.id == id:
            return {"evento":evento}
    return {"mensaje":"evento no encontrado"}

@app.get('/eventos_realizados', response_model=list[Evento])
async def read_eventos_realizados(token: Annotated[str, Depends(oauth2_scheme)]) -> list[Evento]:
    if len(eventos_list) < 1:
        raise HTTPException(status_code=404, detail="No existen eventos agregados")

    eventos_realizados = list(filter(lambda e: e.fue_realizado == True, eventos_list))
    return eventos_realizados

@app.get('/eventos_norealizados', response_model=list[Evento])
async def read_eventos_norealizados(token: Annotated[str, Depends(oauth2_scheme)]) -> list[Evento]:
    if len(eventos_list) < 1:
        raise HTTPException(status_code=404, detail="No existen eventos agregados")

    eventos_norealizados = list(filter(lambda e: e.fue_realizado == False, eventos_list))
    return eventos_norealizados


@app.put('/eventos/{id}')
async def update_evento(id:int, eventoB: Evento, token: Annotated[str, Depends(oauth2_scheme)]):
    for index, evento in enumerate(eventos_list):
        if evento.id == id:
            eventos_list[index] = eventoB
            eventos_list[index].id = id
            return {"evento": eventos_list[index]}
    return {"mensaje":"evento no encontrado"}

@app.put('/eventos/agregar_nota/{id}')
async def update_notaevento(id:int, nota: str):
    for index, evento in enumerate(eventos_list):
        if evento.id == id:
            eventos_list[index].notas_evento.append(nota)
            return {"mensaje": "nota agregada"}
    return {"mensaje":"evento no encontrado"}

@app.delete('/eventos/{id}')
async def delete_evento(id:int, token: Annotated[str, Depends(oauth2_scheme)]):
    for index, evento in enumerate(eventos_list):
        if evento.id == id:
            if evento.fue_realizado:
                return {"message":"no puedes eliminar un evento que ya fue realizado"}
            else:
                del eventos_list[index]
                return {"message":"evento eliminado"}
    return {"message":"evento no encontrada"}













