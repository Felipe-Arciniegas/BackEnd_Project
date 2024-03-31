from fastapi import FastAPI , Body , Path , Query , Request , HTTPException , Depends
from fastapi.responses import HTMLResponse , JSONResponse
from typing import List, Optional
from pydantic import BaseModel, Field
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
#from config.database import Session, engine, Base
#from models.movie import Movie as MovieModel

# Creando una instancia de la clase FastAPI
app = FastAPI()
#Base.metadata.create_all(bind=engine)

# Cambios a la documentacion
app.title = "Mi Super Api"
app.version = "V2.0.0"

class User(BaseModel):
    email: str
    password: str

class Movie(BaseModel): 
    id: Optional[int] = None
    title: str = Field(min_length=2, max_length=200, default="Mi Pelicula")
    overview: str = Field(default= "Descripcion Pelicula", min_length=20, max_length=350)
    year: int = Field(default=2024, le=2024)
    rating: float = Field(ge=0, le=10, default=10)
    category: str = Field(default="Comedia", min_length=5, max_length=20)

    # Configuracion de la documentacion
    class Config:
        model_config = {
        "json_schema_extra": {
                "examples": [
                    {
                        "id": 1,
                        "title": "Mi Pelicula",
                        "overview": "Descripcion de la pelicula",
                        "year": 2022,
                        "rating": 9.9,
                        "category": "Acción"
                    }
                ]
            }
        }

movies = [
    {
        "id" :1,
        "title" : "Avatar",
        "overview" : "Simios azules extraterrestres que pelean por el poder de la naturaleza",
        "year" : 2009,
        "rating" : 9.1,
        "category" : "Fiction"

    },
    {
        "id" :2,
        "title" : "Piratas del caribe",
        "overview" : "Piratas del Caribe es el título de una franquicia cinematográfica de aventura fantástica y piratas, La saga Piratas del Caribe cuenta con cinco películas estrenadas y una sexta en producción. Los directores de las películas han sido: Gore Verbinski, Rob Marshall, y Joachim Rønning y Espen Sandberg ",
        "year" : 2003,
        "rating" : 7.2,
        "category" : "Piratas"

    },
    {
        "id" :3,
        "title" : "Piratas del caribe: el cofre de la muerte",
        "overview" : "Cuando el fantasmal pirata Davy Jones llega a cobrar una deuda sangrienta, el Capitán Jack Sparrow debe encontrar la forma de evitar su destino y que su alma sea maldecida para siempre. No obstante, el astuto fantasma logra interrumpir los planes nupciales de los amigos de Jack, Will Turner y Elizabeth Swann. ",
        "year" : 2006,
        "rating" : 6.4,
        "category" : "Piratas"

    },
]
class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=401, detail="Invalid user")
        #return 

#Primer End Point
@app.get("/", tags=["Home"])
def message():
    return HTMLResponse(
        content="<h1>Bienvenido a mi Super Api</h1>"
    )

@app.get("/movies", tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=200, content=movies)

#Segundo End Point
@app.get("/movies/{id}", tags=['movies'], response_model=Movie, status_code=200)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie: # se cambia y se dice que es igual a Path(int)
    movie = list(filter(lambda movie: movie['id'] == id, movies))
    if len(movie) > 0:
        result = JSONResponse(content=movie, status_code=200)
    else:
        result = JSONResponse(content={"message": "Movie not found"}, status_code=404)
    return result

#Tercer End Point
@app.get("/movies/", tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=3, max_length=15)) -> List[Movie]:
    movies_by_category = [movie for movie in movies if movie['category'] == category]
    return JSONResponse(content=movies_by_category)

#Cuarto End Point
@app.post("/movies", tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    movies.append(movie)
    return JSONResponse(content={"message": "Movie created successfully"}, status_code=201)

@app.put("/movies/{id}", tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    for movie in movies:
        if movie['id'] == id:
            movie['title'] = movie.title
            movie['overview'] = movie.overview
            movie['year'] = movie.year
            movie['rating'] = movie.rating
            movie['category'] = movie.category
    return JSONResponse(content={"message": "Movie updated successfully"}, status_code=200)

@app.delete("/movies/{id}", tags=['movies'], response_model=dict)
def delete_movie(id: int) -> dict:
    for movie in movies:
        if movie['id'] == id:
            movies.remove(movie)
    return JSONResponse(content={"message": "Movie deleted successfully"})

@app.post("/login", tags=['auth'], response_model=dict, status_code=200)
def login(user: User) -> dict:
    if user.email == "admin@gmail.com" and user.password == "admin":
        token = create_token(data=user.model_dump())
        return JSONResponse(content={"token": token}, 
                            status_code=200)
    else:
        return JSONResponse(content={"message": "Invalid credentials"},
                            status_code=401)