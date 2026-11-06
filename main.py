from fastapi import FastAPI

from controller.auth_controller import router as auth_router
from controller.producto_controller import router as producto_router
from db.database import crear_tablas

app = FastAPI(lifespan=crear_tablas)

app.include_router(auth_router)
app.include_router(producto_router)
