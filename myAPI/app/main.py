from fastapi import FastAPI
from app.routers import usuarios, varios
from app.data.db import engine
from app.data import usuario 

usuario.Base.metadata.create_all(bind=engine)

# ==================INSTANCIA DEL SERVIDOR==================
app = FastAPI(
    title="¿Cómo tu te llamah?, yo no sé",
    description= 'Fidel Juárez',
    version='1.0.0'
    )
app.include_router(usuarios.router)
app.include_router(varios.router)
# =================TB FICTICIA  ==================

# =================VALIDACIONES =============
#==================SEGURIDAD    ===============
#==================ENDPOINTS    ==================










