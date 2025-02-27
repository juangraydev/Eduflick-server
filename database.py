from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Field, Session, select
from fastapi import FastAPI, Depends

DATABASE_URL = "sqlite:///./test.db"  # SQLite database URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()
Base = declarative_base()

# Create the database tables
SQLModel.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()