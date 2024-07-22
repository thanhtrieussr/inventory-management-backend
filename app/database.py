# app/database.py
# Author: Thanh Trieu
# Description: Contains database setup and session management for SQLAlchemy.

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends

# Load environment variables from a .env file if present
load_dotenv()

# Fetch the database URL from environment variables
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

# Create the SQLAlchemy engine, which will interface with the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for our models to inherit from
Base = declarative_base()

def get_db() -> Session:
    """Dependency for providing a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
