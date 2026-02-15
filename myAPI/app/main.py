from fastapi import FastAPI, status, HTTPException
import asyncio
from typing import Optional

# ==================INSTANCIA DEL SERVIDOR==================
app = FastAPI(
    title="¿Cómo tu te llamah?, yo no sé",
    description= 'Fidel Juárez',
    version='1.0.0'
    )

# ==================TB FICTICIA ==================

usuarios=[
    {"id":1, "nombre":"Juan","edad":21 },
    {"id":2, "nombre":"Israel","edad":21 },
    {"id":3, "nombre":"Sofi","edad":21 },
]

#================== ENDPOINTS==================

@app.get("/", tags=['Inicio'])
async def bienvenida():
    return{"Mensaje": "!Bienvenido a mi API"}

@app.get("/HolaMundo", tags=['Bienvenida Asíncrona '])
async def hola():
    await asyncio.sleep(1)  #Lo mandas a dormir || SIMULACIÓN DE UNA PETICIÓN
    return{
        "mensaje":"!Bienvendio a mi API ",
        "Estatuos":"200"
        }
@app.get("/v1/usuario/ {id}", tags=['Parametro Obligatorio'])
async def consultaUno(id:int):
    return{"Se encontro usuario": id}

@app.get("/v1/parametroOp/", tags=['Parametro Opcional'])
async def consultaTodos(id:Optional[int]=None):
    if id is not None:
        for usuariok in usuarios:
            if usuariok["id"] == id:
                return{"mensaje": "usuario encontrado", "usuario": usuariok}
        return{"mensaje": "usuario no encontrado","usuario":id}
    else:
        return{"mensaje": "No se proporciono id" }


@app.get("/v1/usuarios/", tags=['CRUD HTTP'])
async def leer_usuarios():
    return{
        "status":"200",
        "total":len(usuarios),
        "usuarios":usuarios
    }

#ENDPOINT TIPO POST
@app.post("/v1/usuarios/", tags=['CRUD HTTP'])
async def crear_usuarios(usuario:dict):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
    usuarios.append(usuario)
    return{
        "status":"200",
        "total":len(usuarios),
        "usuarios":usuarios
    }

#ENDPOINT TIPO PUT
@app.put("/v1/usuarios/", tags=['CRUD HTTP'])
async def actualizar_usuarios(usuario:dict):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            usuario.update(usuario) 
            return {
                "status": "200",
                "mensaje": "Usuario actualizado",
                "usuario": usuario
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )
    
@app.delete("/v1/usuarios/{id}", tags=['CRUD HTTP'])
async def eliminar_usuario(id: int):
    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return {
                "status": "200",
                "mensaje": "Usuario eliminado",
                "usuario": usr
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )

