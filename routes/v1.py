from utils.helper_functions import upload_image_to_server
from utils.db_functions import db_check_personel, db_get_author, db_get_author_from_id, db_get_book_with_isbn, db_insert_personel, db_patch_author_name
from models.book import Book
from models.author import Author
from models.user import User
from models.jwt_user import JWTUser
from fastapi import FastAPI, Body, File, Header, Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED
from starlette.responses import Response
from utils.security import authenticate_user, create_jwt_token, check_jwt_token
import utils.redis_object as re

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
async def post_user(user: User):
    await db_insert_personel(user)
    #return {"request-body": user, "request custom header": x_custom}
    return {"result": "personel is created"}

@app_v1.post("/login", tags=['User'])
async def get_user_validation(username: str = Body(...), password: str = Body(...)):
    redis_key = f"{username},{password}"
    result = await re.redis.get(redis_key)

    # Redis has the data
    if result:
        print(bool(result))
        if bool(result) == True:
            return {"is_valid (redis)": True}
        else: 
            return {"is_valid (redis)": False}
    
    # Redis does not have the data
    else:
        result = await db_check_personel(username, password)
        await re.redis.set(redis_key, str(result), expire=10)
    
        return {"is_valid (db)": result}

@app_v1.get("/book/{isbn}", response_model=Book, response_model_include=["name", "year"], tags=['Book'])
async def get_book_with_isbn(isbn: str):
    book = await db_get_book_with_isbn(isbn)
    author = await db_get_author(book['author'])
    book['author'] = Author(**author)
    result = Book(**book)
    return result 

@app_v1.get("/author/{id}/book", tags=['Book'])
async def get_author_books(id: int, order: str = "asc"):
    author = await db_get_author_from_id(id) 
    if author is not None:
        books = author['books']
        if order == "asc":
            books = sorted(books)
        else:
            books = sorted(books, reverse=True)
        return {"books": books}
    else:
        return {"no author with corresponding id"}

@app_v1.patch("/author/{id}/name", tags=['Book'])
async def patch_author_name(id: int, name: str = Body(..., embed=True)):
    await db_patch_author_name(id, name)
    return {"result": "Name is updated"}

@app_v1.post("/user/author", tags=['Book'])
async def post_user_and_author(user: User, author: Author, bookstore_name: str = Body(..., embed=True)):
    return{"User": user, "Author": author, "bookstore_name": bookstore_name}

@app_v1.post("/user/photo", tags=['User'])
async def upload_photo(response: Response, profile_photo: bytes = File(...)):
    response.headers['x-file-size'] = str(len(profile_photo))
    response.set_cookie(key="cookie-api", value="test")
    await upload_image_to_server(profile_photo)
    return {"file_size": len(profile_photo)}


