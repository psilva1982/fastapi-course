from utils.constants import DOC_BOOK_ISBN
from pydantic.fields import Field
from models.author import Author
from pydantic import BaseModel

class Book(BaseModel):
    isbn: str = Field(None, description=DOC_BOOK_ISBN)
    name: str 
    author: Author
    year: int = Field(None, gt=1900, lt=2100)
