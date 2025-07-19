from environs import Env
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

env = Env()
env.read_env()
db_url = env.str("DATABASE_URL")

engine = create_engine(db_url)
Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)

base = declarative_base()


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
