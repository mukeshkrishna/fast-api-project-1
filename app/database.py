from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
import psycopg2
from psycopg2.extras import RealDictCursor
import time

#  "postgresql://<username>:<password>@<ip-address/hostname>/<database_name>"
SQLALCHEMY_DATABASE_URL = (f"postgresql://{settings.database_username}:{settings.database_password}@"
                           f"{settings.database_hostname}:{settings.database_port}/{settings.database_name}")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base = declarative_base()

# this function to get a session to DB, so for every request we will create a session to postgres
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
#
# while True:
#     try:
#         # create postgres connection
#         # cursor_factory=RealDictCursor - this gives the column name, and returns a python dictionary
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='postgres', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successfull")
#         break
#     except Exception as error:
#         print("Connecting to Database Failed")
#         print("Error: ", error)
#         time.sleep(5) # sleep for 5 seconds
#
# my_posts = [{"id": 1,"title": "title of post 1", "content": "content of post 1"},
#             {"id": 2,"title": "title of post 2", "content": "content of post 2"}]