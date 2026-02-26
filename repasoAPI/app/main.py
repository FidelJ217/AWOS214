from fastapi import FastAPI, status, HTTPException
import asyncio
from typing import Optional
from pydantic import BaseModel, Field

# ==================INSTANCIA DEL SERVIDOR==================
app = FastAPI(
    title="PRÁCTICA NO.5",
    description= 'Repaso del uso de API',
    version='1.0.0'
    )

# ==================TB FICTICIA ==================
usuarios=[
    {"id":1, "nombre":"Juan","edad":21, "correo":"1234@upq.edu.mx" },
    {"id":2, "nombre":"Israel","edad":21,"correo":"1234@upq.edu.mx"},
    {"id":3, "nombre":"Sofi","edad":21 ,"correo":"1234@upq.edu.mx"},
]

books=[
    {"id":1, "titulo":"Harry Potter","estado":"Prestado","ano": 1997,"paginas": 300 },
    {"id":2, "titulo":"Orgullo y prejuicio", "estado":"Disponible","ano": 1813, "paginas":220},
    {"id":3, "titulo":"La cancion de Aquiles", "estado":"Disponible","ano": 2011, "paginas":400},
]

prestamos = []

class books_register(BaseModel):
    id: int=Field(...,gt=0,description="Identificacion del libro")
    titulo:str=Field(...,min_length=2,max_length=100,example="El gato negro")
    estado:str=Field(...,min_length=8,max_length=20,description="Estado actual del libro",example="Prestado o Disponible")
    ano:int=Field(...,gt=1450,le=2026,example=2026)
    paginas:int=Field(...,gt=1,example="El libro debe de contar con mas de una pagina")



class usuario_register(BaseModel):
    id: int =Field(...,gt=0,description="Identificación de usuario")
    nombre:str = Field(...,min_legth=3,max_length=50, example="Juanita")
    edad: int =Field(...,ge=1,le=123,description="Edad valida entre 1 y 123")


class prestamo_register(BaseModel):
    id_libro: int = Field(..., gt=0)
    id_usuario: int = Field(..., gt=0)
#================== ENDPOINTS==================

@app.get("/", tags=['Inicio'])
async def bienvenida():
    return{"Mensaje": "!Bienvenido a mi API"}



@app.get("/v1/books/", tags=['CRUD HTTP'])
async def listar_books():
    return{
        "status":"200",
        "total":len(books),
        "usuarios":books
    }
#LIBROS DISPONIBLES LOL
@app.get("/v1/books/disponibles", tags=['Disponible'])
async def books_disponibles():
    disponibles = [bks for bks in books if bks["estado"] == "Disponible"]
    return {
        "total": len(disponibles),
        "books": disponibles
    }
#LIBROS POR TITULO LOL
@app.get("/v1/books/buscar/{titulo}", tags=['Titulo'])
async def buscar_book(titulo: str):

    resultado = []

    for bks in books:
        if titulo.lower() in bks["titulo"].lower():
            resultado.append(bks)

    if len(resultado) == 0:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    return {
        "total": len(resultado),
        "books": resultado
    }
#LIBRO REGISTRAR
@app.post("/v1/books/", tags=['Registrar'])
async def registrar_books(book:books_register):
    for bks in books:
        if bks["id"] == book.id:
            raise HTTPException(
                status_code=409,
                detail="El id ya existe"
            )
    books.append(book)
    return{
        "status":"201",
        "total":len(books),
        "books":books
    }

#LIBRO PRESTADO
@app.post("/v1/prestamos/", tags=['Prestamos'])
async def registrar_prestamo(data: prestamo_register):
    for bks in books:
        if bks["id"] == data.id_libro:
            if bks["estado"] != "Disponible":
                raise HTTPException(status_code=409, detail="Libro no disponible")
            bks["estado"] = "Prestado"
            prestamo = {
                "id_libro": data.id_libro,
                "id_usuario": data.id_usuario
            }

            prestamos.append(prestamo)

            return {
                "mensaje": "Prestamo registrado",
                "prestamo": prestamo
            }

    raise HTTPException(status_code=404, detail="Libro no encontrado")

#LIBRO DEVOLVIDO
@app.put("/v1/prestamos/devolver/{id_libro}", tags=['DevolvidoLibro'])
async def devolver_libro(id_libro: int):

    for bks in books:
        if bks["id"] == id_libro:
            bks["estado"] = "Disponible"
            return {"mensaje": "Libro devuelto"}

    raise HTTPException(status_code=404, detail="Libro no encontrado")

#ELIMINASAO
@app.delete("/v1/prestamos/{id_libro}", tags=['Prestamos'])
async def eliminar_prestamo(id_libro: int):

    for pr in prestamos:
        if pr["id_libro"] == id_libro:
            prestamos.remove(pr)
            return {"mensaje": "Prestamo eliminado"}

    raise HTTPException(status_code=404, detail="Prestamo no encontrado")