from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

#Definimos la URL de la BASE DE DATOS

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://admin:123456@postgres:5432/DB_miapi" 
)

#2.Crearemos el motor de conexión
engine= create_engine(DATABASE_URL)

#3.Crearemos gestionador de sesiones
SessionLocal = sessionmaker(
    autocommit= False,
    autoflush= False,
    bind= engine
)

#4. Base Declarativa para modelos
Base= declarative_base()

#5. Función para la sesión en cada peticion D
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()