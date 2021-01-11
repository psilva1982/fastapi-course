from utils.pure_db import fetch, execute 

async def db_check_jwt_user(user):
    query = """ select * from users where username = :username and password = :password """
    values = { "username": user.username, "password": user.password }

    result = await fetch(query, True, values)
    print(user)
    if result is None:
        return False
    else:
        return True

async def db_check_token_username(username):
    query = """ select * from users where username = :username """
    values = { "username": username }

    result = await fetch(query, True, values)
    if result is None:
        return False
    else:
        return True