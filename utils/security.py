import jwt
from fastapi import Depends, HTTPException
from datetime import datetime as dt, timedelta
import time
from passlib.context import CryptContext
from models.jwt_user import JWTUser
from utils.constants import JWT_EXPIRATION_TIME_MINUTES, JWT_ALGOTITH, JWT_SECRET_KEY
from fastapi.security import OAuth2PasswordBearer
from starlette.status import HTTP_401_UNAUTHORIZED

pwd_context = CryptContext(schemes=["bcrypt"])
oauth_schema = OAuth2PasswordBearer(tokenUrl='/token')

jwt_user1 = {"username": "test", "password": "$2b$12$xAWrWRhXfCVKgYAItl0JI.bVsz/3NZ4Ivfc1FtUtNzRJLlK7.aWXS", "active": True, "role": "admin"}
fake_user1 = JWTUser(**jwt_user1)

jwt_user2 = {"username": "test2", "password": "$2b$12$xAWrWRhXfCVKgYAItl0JI.bVsz/3NZ4Ivfc1FtUtNzRJLlK7.aWXS", "active": True, "role": "admin"}
fake_user2 = JWTUser(**jwt_user2)

jwt_user3 = {"username": "test3", "password": "$2b$12$xAWrWRhXfCVKgYAItl0JI.bVsz/3NZ4Ivfc1FtUtNzRJLlK7.aWXS", "active": False, "role": "admin"}
fake_user3 = JWTUser(**jwt_user3)

jwt_user_fake_db = [fake_user1, fake_user2, fake_user3]

def get_hashed_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Authenticate username and password to give JWT
def authenticate_user(user: JWTUser):
    if fake_user1.username == user.username:
        if verify_password(user.password, fake_user1.password):
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
def check_jwt_token(token: str = Depends(oauth_schema)):
    try:
        jwt_payload = jwt.decode(token, JWT_SECRET_KEY, algorithm=JWT_ALGOTITH)
        username = jwt_payload.get('sub')
        role = jwt_payload.get('role')
        expiration = jwt_payload.get('exp')

        if time.time() < expiration:
            if fake_user1.username == username:
                return final_checks(role)

    except Exception as e:
        return False
        #raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

    #raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
    return False

# Last checking and returning the final result 
def final_checks(role: str):
    if role == "admin":
        return True
    else:
        return False 