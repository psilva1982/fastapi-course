from utils.constants import DB_URL, TESTING, TEST_DB_URL
from databases import Database

if TESTING:
    db = Database(TEST_DB_URL)
    
else:
    db = Database(DB_URL)