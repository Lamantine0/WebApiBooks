from pydantic import BaseModel

class Book_DTO(BaseModel):

    
    title : str

    author : str

    publication_year : int

    genre : str


class Book_genre(BaseModel):

    
    title : str

    genre : str    