from models.book import Book
from models.author import Author
from models.user import User
from models.jwt_user import JWTUser
from fastapi import FastAPI, Body, File, Header, Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED
from starlette.responses import Response
from utils.security import authenticate_user, create_jwt_token, check_jwt_token

app_v1 = APIRouter()

# @app_v1.post("/token")
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     jwt_user_dict = {"username": form_data.username, "password": form_data.password }
#     jwt_user = JWTUser(**jwt_user_dict)

#     user = authenticate_user(jwt_user)
#     if user is None:
#         raise HTTPException(status_code=HTTP_401_UNAUTHORIZED) 
    
#     jwt_token = create_jwt_token(user)
#     return {"access_token": jwt_token}


@app_v1.get("/hello")
async def hello_world():
    return {"Hello World"}

@app_v1.post("/user", status_code=HTTP_201_CREATED, tags=['User'])
async def post_user(user: User, x_custom: str = Header('default'), jwt: bool = Depends(check_jwt_token)):
    return {"request-body": user, "request custom header": x_custom}

@app_v1.get("/user", tags=['User'])
async def get_user_validation(password: str):
    return {"query_parameter": password}

@app_v1.get("/book/{isbn}", response_model=Book, response_model_include=["name", "year"], tags=['Book'])
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

@app_v1.get("/author/{id}/book", tags=['Book'])
async def get_author_books(id: int, category: str, order: str = "asc"):
    return {"query changable parameter": order + category + str(id)}

@app_v1.patch("/author/name", tags=['Book'])
async def patch_author_name(name: str = Body(..., embed=True)):
    return {"name in body": name}

@app_v1.post("/user/author", tags=['Book'])
async def post_user_and_author(user: User, author: Author, bookstore_name: str = Body(..., embed=True)):
    return{"User": user, "Author": author, "bookstore_name": bookstore_name}

@app_v1.post("/user/photo", tags=['User'])
async def upload_photo(response: Response, profile_photo: bytes = File(...)):
    response.headers['x-file-size'] = str(len(profile_photo))
    response.set_cookie(key="cookie-api", value="test")
    return {"file_size": len(profile_photo)}

