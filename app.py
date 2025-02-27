from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Field, Session, select
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import get_db, engine
from models import User
from datetime import datetime, timedelta
import bcrypt
import jwt

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
        
app = FastAPI()

origins = [
    "http://localhost:3000",  # ReactJS development server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# @app.on_event("startup")
# async def startup():
#     await database.connect()

# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()

# Root route
@app.get("/")
def root():
    return {"message": "Welcome to the root route!"}

class LoginModel(BaseModel):
    email: str
    password: str

@app.post("/api/login")
async def login(data: LoginModel, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.email == data.email).first()

        if not user or not bcrypt.checkpw(data.password.encode('utf-8'), user.password.encode('utf-8')):
            raise HTTPException(status_code=400, detail="Invalid email or password")

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={
                "id": user.id,
                "username": user.username,
                "email": user.email
            }, expires_delta=access_token_expires
        )

        return {
            "status": "200",
            "message": "Login successful",
            "data": {
                "access_token": access_token,
                "token_type": "bearer"
            }
        }
    except Exception as e:
        return {
            "status": '500',
            "message": str(e)
        }

class SignUpModel(BaseModel):
    username: str
    email: str
    password: str

@app.post("/api/signup")
async def create_user(data: SignUpModel, db: Session = Depends(get_db)):
    try:
        # Check if the email or username already exists
        query = select(User).where((User.email == data.email) | (User.username == data.username))
        existing_user = await database.fetch_one(query)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email or username already registered")

        # Insert the new user into the database
        new_user = User(username=data.username, email=data.email, password=bcrypt.hashpw(data.password.encode('utf-8'), bcrypt.gensalt()))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {
            "status": "200",
            "message": "User created successfully",
        }
    except Exception as e:
        return {
            "status": '500',
            "message": str(e)
        }