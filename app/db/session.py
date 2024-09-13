from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# from core.config import settings
# from app.core.config import settings
# import os
# SQL_DATABASE_URL = os.environ.get('DATABASE_URI')

engine = create_engine("postgresql://postgres:Akif1432@localhost/auth")

SessionLocale = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
