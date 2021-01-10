from models.book import Book
from models.author import Author
from fastapi.params import Body, File, Header 
from models.user import User
from fastapi import FastAPI, APIRouter
from starlette.status import HTTP_201_CREATED
from starlette.responses import Response

app_v2 = APIRouter()

@app_v2.get("/hello")
async def hello_world():
    return {"Hello World"}

@app_v2.post("/user", status_code=HTTP_201_CREATED)
async def post_user(user: User, x_custom: str = Header(...)):
    return {"request-body": user, "request custom header": x_custom}

@app_v2.get("/user")
async def get_user_validation(password: str):
    return {"v2 get users"}

@app_v2.get("/book/{isbn}", response_model=Book, response_model_include=["name", "year"])
async def get_book_with_isbn(isbn: str):
    author_dict = {
        "name": "Author",
        "books": ["book1", "book2"]
    }
    book_dict = {
        "isbn": "isb1",
        "name": "book1",
        "year": 2019,
        "author": Author(**author_dict)
    }
    book1 = Book(**book_dict)
    return book1

@app_v2.get("/author/{id}/book")
async def get_author_books(id: int, category: str, order: str = "asc"):
    return {"query changable parameter": order + category + str(id)}

@app_v2.patch("/author/name")
async def patch_author_name(name: str = Body(..., embed=True)):
    return {"name in body": name}

@app_v2.post("/user/author")
async def post_user_and_author(user: User, author: Author, bookstore_name: str = Body(..., embed=True)):
    return{"User": user, "Author": author, "bookstore_name": bookstore_name}

@app_v2.post("/user/photo")
async def upload_photo(response: Response, profile_photo: bytes = File(...)):
    response.headers['x-file-size'] = str(len(profile_photo))
    response.set_cookie(key="cookie-api", value="test")
    return {"file_size": len(profile_photo)}

