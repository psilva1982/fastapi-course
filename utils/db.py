from utils.constants import DB_HOST, DB_PASS, DB_USER
from databases import Database

async def connect_db():
    db = Database(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/bookstore")
    await db.connect()
    return db

async def disconnect_db(db):
    await db.disconnect()

async def execute(query, is_many, values=None):
    db = await connect_db()
    
    if is_many:
        await db.execute_many(query=query, values=values)
    
    else:
        await db.execute(query=query, values=values)
    
    await disconnect_db(db)

async def fetch(query, is_one, values=None):
    db = await connect_db()
    
    if is_one:
        result = await db.fetch_one(query=query, values=values)
        out = dict(result)
    
    else:
        result = await db.fetch_all(query=query, values=values)
        out = []
        for row in result:
            out.append(dict(row))

    await disconnect_db(db)
    return out
