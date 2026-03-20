from fastapi import Depends, FastAPI, status, HTTPException
import asyncio
from pydantic import BaseModel, Field
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime,timedelta


#==================CONFIGURACIÓN JWT ==================

SECRET_KEY = "1234"
ALGORITHM =  "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#==================CREACION DE ESQUEMA OAUTH2 ==================

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

#==================CREAR TOKEN==================

def crear_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes = 15)
    
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt

# ==================INSTANCIA DEL SERVIDOR==================
app = FastAPI(
    title="Usando Ouath2 + JWT",
    description= 'Fidel Juárez',
    version='1.0.0'
    )

# ==================TB FICTICIA ==================

usuarios=[
    {"id":1, "nombre":"Juan","edad":21 },
    {"id":2, "nombre":"Israel","edad":21 },
    {"id":3, "nombre":"Sofi","edad":21 },
]

# ==================USUARIO DE PRUEBA==================
user_db = {
    'Fidel': {
        "username": "Fidel",
        "password": "1234"
    }
}

# ==================VALIDACIONES PYNDATIC ==================
class usuario_create(BaseModel):
    id: int =Field(...,gt=0,description="Identificación de usuario")
    nombre:str = Field(...,min_length=3,max_length=50, example="Juanita")
    edad: int =Field(...,ge=1,le=123,description="Edad valida entre 1 y 123")


class usuario_delete(BaseModel):
    id: int =Field(...,gt=0,description="Identificación de usuario")


#================== LEER TOKEN==================
async def obtener_usuario(token: str = Depends(oauth2_scheme)):

    credenciales_exception = HTTPException(
        status_code=401,
        detail="Token inválido"
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise credenciales_exception

    except JWTError:
        raise credenciales_exception

    return username

#==================ENDPOINT GET==================
@app.get("/v1/usuarios/", tags=['CRUD HTTP'])
async def leer_usuarios():
    return{
        "status":"200",
        "total":len(usuarios),
        "usuarios":usuarios
    }

#==================ENDPOINT POST==================
@app.post("/v1/usuarios/", tags=['CRUD HTTP'])
async def crear_usuarios(usuario:usuario_create):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
    usuarios.append(usuario.dict())
    return{
        "status":"200",
        "total":len(usuarios),
        "usuarios":usuarios
    }

#==================ENPOINT PUT==================
@app.put("/v1/usuarios/", tags=['CRUD HTTP'])
async def actualizar_usuarios(usuario:dict):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            usr.update(usuario) 
            return {
                "status": "200",
                "mensaje": "Usuario actualizado",
                "usuario": usr
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )

#==================ENPOINT DELETE==================    
@app.delete("/v1/usuarios/{id}", tags=['CRUD HTTP'])
async def eliminar_usuario(
    id: int,
    usuario_actual: str = Depends(obtener_usuario)
):
    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return {
                "status": "200",
                "mensaje": f"Usuario eliminado por {usuario_actual}",
                "usuario": usr
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):

    user = user_db.get(form_data.username)

    if not user:
        raise HTTPException(status_code=400, detail="Usuario incorrecto")

    if form_data.password != user["password"]:
        raise HTTPException(status_code=400, detail="Password incorrecto")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = crear_token(
        data={"sub": user["username"]},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

