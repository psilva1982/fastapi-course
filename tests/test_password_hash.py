from utils.security import get_hashed_password

def test_password_hash():
    print(get_hashed_password('test'))