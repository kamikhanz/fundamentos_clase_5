from fastapi import APIRouter, HTTPException, status

from db.database import SessionDep
from dependencies.auth import CurrentUser
from schemas.producto import ProductoCreate, ProductoRead, ProductoUpdate
from services.producto_service import (
    actualizar_producto,
    crear_producto,
    eliminar_producto,
    obtener_producto,
    obtener_productos,
)

router = APIRouter(tags=["productos"], prefix="/productos")


@router.post("/")
def create_producto(
    data: ProductoCreate, current_user: CurrentUser, session: SessionDep
):
    return crear_producto(data, current_user.id, session)


@router.get("/", response_model=list[ProductoRead])
def get_productos(current_user: CurrentUser, session: SessionDep):
    return obtener_productos(session, current_user)


@router.get("/{id}")
def get_producto(id: int, current_user: CurrentUser, session: SessionDep):
    producto = obtener_producto(id, current_user.id, session)
    if producto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
        )

    return producto


@router.put("/{id}")
def update_producto(
    id: int, data: ProductoUpdate, current_user: CurrentUser, session: SessionDep
):
    return actualizar_producto(id, data, current_user.id, session)


@router.delete("/{id}")
def delete_producto(id: int, current_user: CurrentUser, session: SessionDep):
    return eliminar_producto(id, current_user.id, session)
