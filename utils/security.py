from utils.db_functions import db_check_jwt_user, db_check_token_username
from fastapi import Depends, HTTPException
from datetime import datetime as dt, timedelta
from jose import jwt
import time
from passlib.context import CryptContext
from models.jwt_user import JWTUser
from utils.constants import JWT_EXPIRATION_TIME_MINUTES, JWT_ALGOTITH, JWT_SECRET_KEY
from fastapi.security import OAuth2PasswordBearer
from starlette.status import HTTP_401_UNAUTHORIZED

pwd_context = CryptContext(schemes=["bcrypt"])
oauth_schema = OAuth2PasswordBearer(tokenUrl='/token')

def get_hashed_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Authenticate username and password to give JWT
async def authenticate_user(user: JWTUser):
    potencial_users = await db_check_jwt_user(user)
    is_valid = False
    for db_user in potencial_users:
        if verify_password(user.password, db_user['password']): 
            is_valid = True 

    if is_valid:
        user.role = "admin"
        return user
    
    return None

# Create access JWT token 
def create_jwt_token(user: JWTUser):
    expiration = dt.utcnow() + timedelta(minutes=JWT_EXPIRATION_TIME_MINUTES)
    jwt_payload = {
        "sub": user.username,
        "role": user.role,
        "exp": expiration
    }
    jwt_token = jwt.encode(jwt_payload, JWT_SECRET_KEY, algorithm=JWT_ALGOTITH)

    return jwt_token

# Check wheather JWT token is correct 
async def check_jwt_token(token: str = Depends(oauth_schema)):
    try:
        jwt_payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGOTITH)
        username = jwt_payload.get('sub')
        role = jwt_payload.get('role')
        expiration = jwt_payload.get('exp')

        if time.time() < expiration:
            is_valid = await db_check_token_username(username)
            if is_valid:
                return final_checks(role)

    except Exception as e:
        print(e)
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

# Last checking and returning the final result 
def final_checks(role: str):
    if role == "admin":
        return True
    else:
        return False 