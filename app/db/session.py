from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# from core.config import settings
# from app.core.config import settings
# import os
# SQL_DATABASE_URL = os.environ.get('DATABASE_URI')
SQL_DATABASE_URL = "postgresql://postgres:admin@localhost/sharify_db"
engine = create_engine(SQL_DATABASE_URL)

SessionLocale = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
