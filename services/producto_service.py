from fastapi import HTTPException
from sqlmodel import select

from db.database import SessionDep
from dependencies.auth import CurrentUser
from models.producto import Producto
from schemas.producto import ProductoCreate, ProductoUpdate


def obtener_productos(session: SessionDep, current_user: CurrentUser):
    return session.exec(select(Producto)).all()


def crear_producto(producto: ProductoCreate, user_id: int, session: SessionDep):
    nuevo_producto = Producto(**producto.model_dump(), user_id=user_id)
    session.add(nuevo_producto)
    session.commit()
    session.refresh(nuevo_producto)
    return nuevo_producto


def obtener_producto(id: int, user_id: int, session: SessionDep):
    return session.exec(
        select(Producto).where(Producto.id == id, Producto.user_id == user_id)
    ).first()


def actualizar_producto(
    id: int, producto: ProductoUpdate, user_id: int, session: SessionDep
):
    producto_existente = session.exec(
        select(Producto).where(Producto.id == id, Producto.user_id == user_id)
    ).first()
    if not producto_existente:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    producto_existente.nombre = producto.nombre
    producto_existente.descripcion = producto.descripcion
    producto_existente.precio = producto.precio
    producto_existente.stock = producto.stock
    session.commit()
    session.refresh(producto_existente)
    return producto_existente


def eliminar_producto(id: int, user_id: int, session: SessionDep):
    producto = session.exec(
        select(Producto).where(Producto.id == id, Producto.user_id == user_id)
    ).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    session.delete(producto)
    session.commit()
    return {"message": "Producto eliminado correctamente"}
