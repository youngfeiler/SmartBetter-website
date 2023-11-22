from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from sshtunnel import SSHTunnelForwarder
import pymysql
import os

# Define your SSH tunnel parameters
ssh_host = os.environ.get('SSH_HOST')
ssh_username = os.environ.get('ssh_username')
ssh_pkey_path = '/Users/stefanfeiler/Desktop/SMARTBETTOR_CODEBASE/SmartBetter-website/test_kp.pem'

# Define your MySQL database parameters
mysql_host = '127.0.0.1'
mysql_port = 3306
mysql_database = os.environ.get('db_name')

class DBManager:
    def __init__(self):
        self.tunnel = SSHTunnelForwarder(
            (ssh_host, 22),
            ssh_username=ssh_username,
            ssh_pkey=ssh_pkey_path,
            remote_bind_address=(os.environ.get('database_endpoint'), 3306),
        )
        self.tunnel.start()  # Start the SSH tunnel
        mysql_uri = f'mysql+pymysql://admin:smartbettor@127.0.0.1:{self.tunnel.local_bind_port}/{mysql_database}'
        self.engine = create_engine(mysql_uri, pool_pre_ping=True, poolclass=QueuePool)
        self.Session = sessionmaker(bind=self.engine)

    def create_session(self):
        return self.Session()
    def get_engine(self):
        return self.engine

    def close(self):
        self.engine.dispose()
        self.tunnel.stop()

db_manager = DBManager()
