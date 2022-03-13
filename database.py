import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))
user = os.environ["POSTGRES_USERNAME"]
password = os.environ["POSTGRES_PASSWORD"]
host = os.environ["POSTGRES_DB_HOST"]
port = os.environ["POSTGRES_DB_PORT"]
db = os.environ["POSTGRES_DB"]

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
