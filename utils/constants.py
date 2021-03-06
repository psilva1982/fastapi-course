from decouple import config
import os 

#openssl rand -hex 32
JWT_SECRET_KEY = "fb43e424da3d616ef40aab5823a9a0b5fa4f822e4c3e485b06a7feb830141c80"
JWT_ALGOTITH = "HS256"
JWT_EXPIRATION_TIME_MINUTES = 5

DOC_TOKEN_SUMARY='Summary of token endpoint'
DOC_TOKEN_DESCRIPTION='Description of token endpoint'

DOC_BOOK_ISBN='It is uniq book id, show is in Schema view'

DB_HOST='localhost'
DB_HOST_PRODUCTION='172.17.0.3'
DB_USER='postgres'
DB_PASS='postgres'
DB_URL=f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/bookstore"
DB_URL_PRODUCTION=f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST_PRODUCTION}:5432/bookstore"


API_IMGBB_KEY=config('API_IMGBB_KEY')
API_IMGBB_URL=f'https://api.imgbb.com/1/upload?key={API_IMGBB_KEY}'

REDIS_URL="redis://localhost"
TEST_REDIS_URL="redis://localhost"
REDIS_URL_PRODUCTION="redis://172.17.0.2"

TESTING = False
IS_LOAD_TEST = False
IS_PRODUCTION = True if os.getenv('PRODUCTION') == "true" else False

TEST_DB_HOST='localhost'
TEST_DB_USER='postgres'
TEST_DB_PASS='postgres'
TEST_DB_URL=f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/test"