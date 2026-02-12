from fastapi import FastAPI
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

@app.get("/v1/usuarios/", tags=['Parametro Opcional'])
async def consultaTodos(id:Optional[int]=None):
    if id is not None:
        for usuariok in usuarios:
            if usuariok["id"] == id:
                return{"mensaje": "usuario encontrado", "usuario": usuariok}
        return{"mensaje": "usuario no encontrado","usuario":id}
    else:
        return{"mensaje": "No se proporciono id" }

