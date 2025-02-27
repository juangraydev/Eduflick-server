from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from databases import Database
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "mysql+pymysql://root:abcd.1234@127.0.0.1:3307/eduflickdb"  # Replace with your MariaDB URL

database = Database(DATABASE_URL)
metadata = MetaData()
Base = declarative_base()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()