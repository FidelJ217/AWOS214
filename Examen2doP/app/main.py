from fastapi import FastAPI, status, HTTPException, Depends
import asyncio
from typing import Optional
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets 


app = FastAPI(
    title="¿Cómo tu te llamah?, yo no sé",
    description= 'Fidel Juárez',
    version='1.0.0'
    )

tickets=[
    {"id":2, "nombre_usuario":"Mouse","descripción":"Trabajar", "prioridad":"Baja", "Estado":"Pendiente" },
    {"id":3, "nombre_usuario":"Teclado","descripción":"Ofimatica", "prioridad":"Media", "Estado":"Pendiente" },
    {"id":4, "nombre_usuario":"Reloj","descripción":"Mirar Reloj", "prioridad":"Alta", "Estado":"Pendiente" },
]

class tickets_register(BaseModel):
    id: int=Field(...,gt=0,description="Identificacion del ticket")
    nombre_usuario:str=Field(...,min_length=20,max_length=200)
    descripción:str=Field(...,min_length=4,max_length=200,,example="Descripción del ticket")
    prioridad:int=Field(...,min_length=4,max_length=5,example="Baja, Media o Alta")

class usuario_delete(BaseModel):
    id: int =Field(...,gt=0,description="Identificación de usuario")

#SEGURIDAD HTTP BASIC
security = HTTPBasic()

def verificar_Peticion(credenciales: HTTPBasicCredentials = Depends(security)):
    userAuth = secrets.compare_digest(credenciales.username, "Fidel")
    passAuth = secrets.compare_digest(credenciales.password, "123456")

    if not (userAuth and passAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no autorizadas"
        )

    return credenciales.username

##TCREAR TICKET
@app.post("v1/tickets/", tags¨['CREAR'])
async def crear_tickets(ticket:dict)
    for ticks in tickets:
        if ticks["id"] = tickets.get("id"):
            raise HTTPException(
                status_code = 400,
                detail = "El id ya existe"
            )
    tickets.append(ticket)
    return{
        "status":"200",
        "total":len(tickets),
        "tickets":tickets
    }

##CONSTULAR POR ID
@app.get("v1/ticker_id/"{id},tags["CONSULTAR  POR ID"])
async def consultar_id(id:int):
    return("Se encontro el ticket": id)

##LISTAR TICKET

@app.get("/v1/tickets/", tags=['CONSULTAR TICKETS'])
async def consultaTodos(id:Optional[int]=None):
    if id is not None:
        for ticks in tickets:
            if ticks["id"] == id:
                return{"mensaje": "Ticket Encontrado", "ticket": ticks}
        return{"mensaje": "usuario no encontrado","ticket":id}
    else:
        return{"mensaje": "No se proporciono id" }

##BORRAR TICKETS

@app.delete("v1/tickets/",tags["BORRAR TICKETS"])
async def borarr_tickets(id:int):
    for ticks in tickets:
        if ticks["id"]= id:
            tickets.remove()ticket
            return{
                "status":"200",
                "mensaje":"Ticket Borrado Con éxito",
                "tickets": tickets
            }

##CAMBIAR ESTADO
@app.put("/v1/prestamos/cambiar_estado/{id}", tags=['CAMBIAR_ESTADO'])
async def Cambiar_Estado(id:int):

    for ticks in books:
        if ticks["id"] == id:
            ticks["Estado"] = "Pendiente"
            return {"mensaje": "Resueltos"}

    raise HTTPException(status_code=404, detail="Libro no encontrado")

