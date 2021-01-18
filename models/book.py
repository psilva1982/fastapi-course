from utils.constants import DOC_BOOK_ISBN
from pydantic.fields import Schema
from models.author import Author
from pydantic import BaseModel, Schema

class Book(BaseModel):
    isbn: str = Schema(None, description=DOC_BOOK_ISBN)
    name: str 
    author: Author
    year: int = Schema(None, gt=1900, lt=2100)
