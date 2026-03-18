# ==================ENDPOINTS ==================
from fastapi import status, HTTPException, Depends, APIRouter
from app.models.usuario import usuario_create
from app.data.database import usuarios
from app.security.auth import verificar_Peticion

#Objeto router que estara instanciado
router = APIRouter(
    prefix="/v1/usuarios", tags=['CRUD HTTP']
)

# ==================Endpoint GET ==================

@router.get("/")
async def leer_usuarios():
    return{
        "status":"200",
        "total":len(usuarios),
        "usuarios":usuarios
    }

# ==================Endpoint POST ==================
@router.post("/", status_code=status.HTTP_200_OK)
async def crear_usuarios(usuario:usuario_create):
    for usr in usuarios:
        if usr["id"] == usuario.id:
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

# ==================Endpoint PUT ==================
@router.put("/")
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

# ==================Endpoint DELETE ==================
    
@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def eliminar_usuario(id: int, userAuth: str = Depends(verificar_Peticion)):
    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return {
                "status": "200",
                "mensaje": f"Usuario eliminado correctamente por: {userAuth}",
                "usuario": usr
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )