from fastapi import FastAPI , Body , Path , Query , Request , HTTPException , Depends
from fastapi.responses import HTMLResponse , JSONResponse
from typing import List, Optional
from pydantic import BaseModel, Field

app = FastAPI()

app.title = "Mi Super Api"
app.version = "V1.0.0"

class Movie(BaseModel): 
    id: Optional[int] = None
    title: str = Field(min_length=2, max_length=200, default="Mi Pelicula")
    overview: str = Field(default= "Descripcion Pelicula", min_length=20, max_length=350)
    year: int = Field(default=2024, le=2024)
    rating: float = Field(ge=0, le=10, default=10)
    category: str = Field(default="Comedia", min_length=5, max_length=20)

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

@app.get("/", tags=["Home"])
def message():
    return HTMLResponse(
        content="<h1>Mi primera chamba</h1>"
    )

@app.get("/movies", tags=["movies"], response_model=List[Movie])
def get_movies():
    return JSONResponse(status_code=200, content=movies)

@app.get("/movies/{id}", tags=["movies"], response_model=Movie)
def get_movies_by_id(id: int):
    for movie in movies:
        if movie ["id"] == id:
            founded_movie = movie
    if not founded_movie:
        return JSONResponse(content={"message":"Movie Not Found"}, status_code=404)
    else:
        return JSONResponse(content=founded_movie, status_code=200)
    

@app.get("/movies/", tags=["movies"])
def get_movies_by_category(category: str):
    movies_filter = [movie for movie in movies if movie ["category"] == category]
    if movies_filter == []:
        return JSONResponse(content={"message":"Movie Not Found"}, status_code=404)
    else:
        return JSONResponse(content=movies_filter, status_code=200)
    


@app.post("/movies", tags=["movies"])
def add_movie(id:int = Body(),title:str = Body(),overview:str = Body(),year:int = Body(),rating:float = Body(),category:str = Body() ):
    movies.append(
        {"id" : id,
         "title" : title,
         "overview" : overview,
         "year" : year,
         "rating" : rating,
         "category" : category
         }
    )
    return movies
    
@app.put("/movies/{id}", tags=["movies"])
def update_movie(id:int,title:str = Body(),overview:str = Body(),year:int = Body(),rating:float = Body(),category:str = Body() ):
    for movie in movies:
        if movie ["id"] == id:
            movie["title"] = title
            movie["overview"] = overview
            movie["year"] = year
            movie["rating"] = rating
            movie["category"] = category
            return movies
        
@app.delete("movies/{id}", tags=["movies"])
def delete_movie(id:int):
    for movie in movies:
        if movie ["id"] == id:
            movies.remove(movie)
            return movies