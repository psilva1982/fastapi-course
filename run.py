from datetime import datetime
from utils.constants import DOC_TOKEN_DESCRIPTION, DOC_TOKEN_SUMARY

from fastapi.exceptions import HTTPException
from models.jwt_user import JWTUser
from fastapi import FastAPI, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from starlette.applications import Starlette
from routes.v1 import app_v1
from routes.v2 import app_v2
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_401_UNAUTHORIZED
from utils.security import authenticate_user, check_jwt_token, create_jwt_token

app = FastAPI(title="Bookstore", description='Course of Fastapi', version='0.0.1')

app.include_router(app_v1, prefix="/v1", dependencies=[Depends(check_jwt_token)])
app.include_router(app_v2, prefix="/v2", dependencies=[Depends(check_jwt_token)])

@app.post("/token", summary=DOC_TOKEN_SUMARY, description=DOC_TOKEN_DESCRIPTION)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    jwt_user_dict = {"username": form_data.username, "password": form_data.password }
    jwt_user = JWTUser(**jwt_user_dict)

    user = await authenticate_user(jwt_user)
    if user is None:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED) 
    
    jwt_token = create_jwt_token(user)
    return {"access_token": jwt_token}


@app.middleware("http")
async def middleware(request: Request, call_next):

    start_time = datetime.utcnow()

    #Modify request here 
    if not any(word in str(request.url) for word in ['/token', '/docs', '/openapi']):
        try:
            jwt_token = request.headers['Authorization'].split('Bearer ')[1]
            is_valid = check_jwt_token(jwt_token)
        except Exception as e:
            is_valid = False
    
        if not is_valid:
            return Response("Unauthorized", status_code=HTTP_401_UNAUTHORIZED)

    response = await call_next(request)
    #Modify response here 
    executation_time = (datetime.now() - start_time).microseconds
    response.headers['x-execution-time'] = str(executation_time)

    return response
