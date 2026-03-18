from fastapi import APIRouter
from typing import Optional
import asyncio
from app.data.database import usuarios

router = APIRouter(
    tags=['Varios']
)


@router.get("/")
async def bienvenida():
    return{"Mensaje": "!Bienvenido a mi API"}

@router.get("/HolaMundo")
async def hola():
    await asyncio.sleep(1)  #Lo mandas a dormir || SIMULACIÓN DE UNA PETICIÓN
    return{
        "mensaje":"!Bienvendio a mi API ",
        "Estatuos":"200"
        }
@router.get("/v1/usuario/ {id}")
async def consultaUno(id:int):
    return{"Se encontro usuario": id}

@router.get("/v1/parametroOp/")
async def consultaTodos(id:Optional[int]=None):
    if id is not None:
        for usuariok in usuarios:
            if usuariok["id"] == id:
                return{"mensaje": "usuario encontrado", "usuario": usuariok}
        return{"mensaje": "usuario no encontrado","usuario":id}
    else:
        return{"mensaje": "No se proporciono id" }