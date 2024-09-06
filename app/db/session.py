from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from core.config import settings
# import os
# SQL_DATABASE_URL = os.environ.get('DATABASE_URI')

engine = create_engine(settings.DATABASE_URL)

SessionLocale = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
