from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


url_databse="postgresql://postgres:pattupara@localhost:5432/expensetracker"
engine=create_engine(url_databse)

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base=declarative_base()


def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()
