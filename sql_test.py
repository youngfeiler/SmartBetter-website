from sshtunnel import SSHTunnelForwarder
import pymysql
import os

with SSHTunnelForwarder(
    (os.environ.get('SSH_HOST')),
    ssh_username=os.environ.get('ssh_username'),
    ssh_pkey="/Users/micahblackburn/Desktop/test_kp.pem",
    remote_bind_address=(os.environ.get('database_endpoint'), 3306)
) as tunnel:
    print("****SSH Tunnel Established****")

    db = pymysql.connect(
        host='127.0.0.1', user="admin",
        password=os.environ.get('mysql_pass'), port=tunnel.local_bind_port
    )

    try:
        # Execute a SQL query to select all records from a table in the 'test' database
        with db.cursor() as cur:
            cur.execute(os.environ.get('db_name'))  # Switch to the 'test' database

            # Add a new row to the 'mytable' table
            # insert_query = "INSERT INTO mytable (id, name, age, email) VALUES (%s, %s, %s, %s)"
            # values = (4, 'Micah', 30, 'john.doe@example.com')
            # cur.execute(insert_query, values)

            # Commit the transaction
            db.commit()

            # Select all records from the 'mytable' table after inserting the new row
            cur.execute('SELECT * FROM mytable')
            
            # Fetch all rows from the result set
            rows = cur.fetchall()

            # Print the retrieved data
            for row in rows:
                print(row)


    finally:
        db.close()

print("YAYY!!")
