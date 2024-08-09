from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Create an in-memory SQLite database
engine = create_engine('sqlite:///:memory:', echo=True)
Session = sessionmaker(bind=engine)