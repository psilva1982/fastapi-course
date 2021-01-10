import asyncio 
from utils.db import execute

query = "insert into books values(:isbn, :name, :author, :year)";
values = [
    {"isbn": "isbn1", "name":"book1", "author":"author1", "year":2019},
    {"isbn": "isbn2", "name":"book2", "author":"author1", "year":2019}
]

loop = asyncio.get_event_loop()
loop.run_until_complete(execute(query, True, values))