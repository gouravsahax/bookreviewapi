from pydantic import BaseModel

class UserReturn(BaseModel):
    id:int
    username:str
    email:str

class FilmReturn(BaseModel):
    name: str
    review: str
    username: str

    class Config:
        from_attributes = True