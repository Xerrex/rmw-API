from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from config import SQLALCHEMY_DATABASE_URI, DATABASE_CONNECT_ARGS


engine = create_engine( SQLALCHEMY_DATABASE_URI, connect_args=DATABASE_CONNECT_ARGS)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
