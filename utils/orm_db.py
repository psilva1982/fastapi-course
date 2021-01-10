from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import ARRAY, Integer, Text
from utils.constants import DB_URL
import sqlalchemy
from sqlalchemy import engine

metadata = sqlalchemy.MetaData()
engine = sqlalchemy.create_engine(DB_URL)
metadata.create_all(engine)

authors = sqlalchemy.Table(
    "authors", metadata, 
    Column("id", Integer, primary_key=True),
    Column("name", Text),
    Column("books", ARRAY(Text)),
)