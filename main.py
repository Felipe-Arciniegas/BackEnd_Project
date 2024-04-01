from fastapi import FastAPI 
from fastapi.responses import HTMLResponse 

from config.database import  engine, Base
from routers.movie import movie_router
from routers.auth import auth_router

# Creando una instancia de la clase FastAPI
app = FastAPI()
Base.metadata.create_all(bind=engine)

# Cambios a la documentacion
app.title = "Mi Super Api"
app.version = "V3.0.0"
app.include_router(movie_router)
app.include_router(auth_router)

#Primer End Point
@app.get("/", tags=["Home"])
def message():
    return HTMLResponse(
        content="<h1>Bienvenido a mi Super Api</h1>"
    )