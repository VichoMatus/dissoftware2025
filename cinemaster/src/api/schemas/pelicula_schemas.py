from pydantic import BaseModel

class PeliculaCreate(BaseModel):
    Title: str
    Duration: int
    Gender: str | None = None
    Image_path: str