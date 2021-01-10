from pydantic import BaseModel

class JWTUser(BaseModel):
    username: str
    password: str 
    active: bool = False
    role: str = None