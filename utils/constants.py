#openssl rand -hex 32
JWT_SECRET_KEY = "fb43e424da3d616ef40aab5823a9a0b5fa4f822e4c3e485b06a7feb830141c80"
JWT_ALGOTITH = "HS256"
JWT_EXPIRATION_TIME_MINUTES = 1

DOC_TOKEN_SUMARY='Summary of token endpoint'
DOC_TOKEN_DESCRIPTION='Description of token endpoint'

DOC_BOOK_ISBN='It is uniq book id, show is in Schema view'

DB_HOST='localhost'
DB_USER='postgres'
DB_PASS='postgres'
DB_URL=f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/bookstore"