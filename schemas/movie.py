from pydantic import BaseModel, Field
from typing import Optional

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