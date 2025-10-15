"""
database.py
------------
Sets up the SQLAlchemy engine and session.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Define the path for the database relative to the backend directory
DB_DIRECTORY = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..', 'data', 'db')
DB_PATH = os.path.join(DB_DIRECTORY, "reddit_data.db")

# Ensure the directory exists
os.makedirs(DB_DIRECTORY, exist_ok=True)

DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
