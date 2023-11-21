from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

DATABASE_URI = 'mysql://user:password@localhost/dbname'  # Replace with your database URI

class DBManager:
    def __init__(self):
        self.engine = create_engine(DATABASE_URI, pool_pre_ping=True, poolclass=QueuePool)
        self.Session = sessionmaker(bind=self.engine)

    def create_session(self):
        return self.Session()

    def close(self):
        self.engine.dispose()

    def create_engine(self):
        return self.engine

db_manager = DBManager()