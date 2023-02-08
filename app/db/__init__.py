from os import getenv # get our environmental variables
from sqlalchemy.ext.declarative import declarative_base # allows us to declare Python classes as database tables
from sqlalchemy import create_engine # lets us create an instance of the SQL Alchemy engine which connects to our database
from sqlalchemy.orm import sessionmaker # manages connection to database and allows us to perform CRUD operations in our database
from dotenv import load_dotenv # load our environmental variables
from flask import g # a global context object that Flask builds and destroys with each request

load_dotenv()

# create the SQL Alchemy engine
engine = create_engine(
    getenv('DB_URL'), 
        echo=True,
        pool_size=20,
        max_overflow=0
    )
# connect the engine to our database connection
Session = sessionmaker(bind=engine)
# used for creating tables in Python
Base = declarative_base()

def init_db(app):
    Base.metadata.create_all(engine) # create all tables

    app.teardown_appcontext(close_db) # run this whenever a request ends

# create a new database connection
def get_db():
    # if the db object does not exist in the global context object created by Flask
    if 'db' not in g:
        g.db = Session() # create a new connection to our database

    return g.db

# close our database connection, runs whenever a request is complete
def close_db(e=None):
    db = g.pop('db', None) # remove the database object from the global context object and set g.db to None

    # if the connection exists, close it
    if db is not None:
        db.close()