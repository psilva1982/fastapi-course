import asyncio 
from utils.pure_db import execute, fetch
from utils.orm_db import authors

query = "insert into books values(:isbn, :name, :author, :year)";
values = [
    {"isbn": "isbn1", "name":"book1", "author":"author1", "year":2019},
    {"isbn": "isbn2", "name":"book2", "author":"author1", "year":2019}
]

loop = asyncio.get_event_loop()
# loop.run_until_complete(execute(query, True, values))

query = "select * from books where isbn=:isbn"
values = {"isbn" : "isbn1"}

query = "select * from books"
#loop.run_until_complete(fetch(query, True, values))
# loop.run_until_complete(fetch(query, False))


async def test_orm():
    # query = authors.insert().values(id=1,name="author1",books=["book1", "book2"])
    # await execute(query, False)

    query = authors.select().where(authors.c.id==1)
    query = await fetch(query, True)
    print(query)


loop.run_until_complete(test_orm())