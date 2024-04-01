from fastapi import FastAPI , Body , Path , Query , Request , HTTPException , Depends
from fastapi.responses import HTMLResponse , JSONResponse
from typing import List, Optional
from pydantic import BaseModel, Field
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
from Config.database import Session, engine, Base
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder

# Creando una instancia de la clase FastAPI
app = FastAPI()
Base.metadata.create_all(bind=engine)

# Cambios a la documentacion
app.title = "Mi Super Api"
app.version = "V2.1.0"

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

@app.get("/movies", tags=['movies'], response_model=List[Movie], status_code=200)#, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

#Segundo End Point
@app.get("/movies/{id}", tags=['movies'], response_model=Movie, status_code=200)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie: # se cambia y se dice que es igual a Path(int)
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if result:
        result = JSONResponse(content=jsonable_encoder(result), status_code=200)
    else:
        result = JSONResponse(content={"message": "Movie not found"}, status_code=404)
    return result

#Tercer End Point
@app.get("/movies/", tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=3, max_length=15)) -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.category == category).all()
    if result:
        result = JSONResponse(content=jsonable_encoder(result), status_code=200)
    else:
        result = JSONResponse(content={"message": "Movie not found"}, status_code=404)
    return result

#Cuarto End Point
@app.post("/movies", tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    new_movie = MovieModel(**movie.model_dump())
    db.add(new_movie)
    db.commit()
    return JSONResponse(content={"message": "Movie created successfully"}, status_code=201)

@app.put("/movies/{id}", tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        response = JSONResponse(content={"message": "Movie not found"}, status_code=404)
    else:
        result.title = movie.title
        result.overview = movie.overview
        result.year = movie.year
        result.rating = movie.rating
        result.category = movie.category
        db.commit()
        response = JSONResponse(content={"message": "Movie updated successfully"}, status_code=200)
    return response

@app.delete("/movies/{id}", tags=['movies'], response_model=dict)
def delete_movie(id: int) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        response = JSONResponse(content={"message": "Movie not found"}, status_code=404)
    else:
        db.delete(result)
        db.commit()
        response = JSONResponse(content={"message": "Movie deleted successfully"})
    return response

@app.post("/login", tags=['auth'], response_model=dict, status_code=200)
def login(user: User) -> dict:
    if user.email == "admin@gmail.com" and user.password == "admin":
        token = create_token(data=user.model_dump())
        return JSONResponse(content={"token": token}, 
                            status_code=200)
    else:
        return JSONResponse(content={"message": "Invalid credentials"},
                            status_code=401)