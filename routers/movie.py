from typing import List
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Path, Query, Depends

from schemas.movie import Movie
from config.database import Session
from models.movie import Movie as MovieModel
from services.movie import MovieService
from middlewares.jwt_bearer import JWTBearer

movie_router = APIRouter()

@movie_router.get("/movies", tags=['movies'], response_model=List[Movie], status_code=200)
def get_movies() -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

#Segundo End Point
@movie_router.get("/movies/{id}", tags=['movies'], response_model=Movie, status_code=200)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    result = MovieService(db).get_movie(id)
    if result:
        result = JSONResponse(content=jsonable_encoder(result), status_code=200)
    else:
        result = JSONResponse(content={"message": "Movie not found"}, status_code=404)
    return result

#Tercer End Point
@movie_router.get("/movies/", tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=3, max_length=15)) -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies_by_category(category)
    if result:
        result = JSONResponse(content=jsonable_encoder(result), status_code=200)
    else:
        result = JSONResponse(content={"message": "Movie not found"}, status_code=404)
    return result

#Cuarto End Point
@movie_router.post("/movies", tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    MovieService(db).create_movie(movie)
    return JSONResponse(content={"message": "Movie created successfully"}, status_code=201)

@movie_router.put("/movies/{id}", tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    movie = MovieService(db).get_movie(id)
    if not movie:
        response = JSONResponse(content={"message": "Movie not found"}, status_code=404)
    else:
        MovieService(db).update_movie(movie)
        response = JSONResponse(content={"message": "Movie updated successfully"}, status_code=200)
    return response

@movie_router.delete("/movies/{id}", tags=['movies'], response_model=dict, dependencies=[Depends(JWTBearer())])
def delete_movie(id: int) -> dict:
    db = Session()
    movie = MovieService(db).get_movie(id)
    if not movie:
        response = JSONResponse(content={"message": "Movie not found"}, status_code=404)
    else:
        MovieService(db).delete_movie(movie)
        response = JSONResponse(content={"message": "Movie deleted successfully"})
    return response