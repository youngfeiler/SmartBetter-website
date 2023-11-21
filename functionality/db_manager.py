from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from sshtunnel import SSHTunnelForwarder

# Define your SSH tunnel parameters
ssh_host = 'ec2-18-221-141-215.us-east-2.compute.amazonaws.com'
ssh_username = 'ec2-user'
ssh_pkey_path = '/Users/micahblackburn/Desktop/test_key.pem'

# Define your MySQL database parameters
mysql_host = '127.0.0.1'  # Localhost because you're tunneling
mysql_port = 3306  # The port on which the MySQL server is exposed locally
mysql_database = 'test'
mysql_uri = f'mysql://user:password@{mysql_host}:{mysql_port}/{mysql_database}'

class DBManager:
    def __init__(self):
        self.tunnel = SSHTunnelForwarder(
            (ssh_host, 22),
            ssh_username=ssh_username,
            ssh_pkey=ssh_pkey_path,
            remote_bind_address=('database-1.cgsvu7bg7jl5.us-east-2.rds.amazonaws.com', 3306),
        )
        self.tunnel.start()  # Start the SSH tunnel
        self.engine = create_engine(mysql_uri, pool_pre_ping=True, poolclass=QueuePool)
        self.Session = sessionmaker(bind=self.engine)

    def create_session(self):
        return self.Session()

    def close(self):
        self.engine.dispose()
        self.tunnel.stop()  # Stop the SSH tunnel when closing the connection
    def create_engine(self):
        return self.engine


db_manager = DBManager()
