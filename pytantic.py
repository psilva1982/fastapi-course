from datetime import datetime
from typing import Dict, List, Tuple, Set 
from pydantic import BaseModel

class Book(BaseModel): 
    name: str
    price: float = 10.0
    year: datetime

book1 = {"name": "book1", "price": 20.0, "year": datetime.now()}

def print_book(book: Book):
    print(book)

def print_name_of_the_book(book_name: str, year: datetime, price: float):
    print(book_name, year, price)

book_object = Book(**book1)
print_book(book_object)