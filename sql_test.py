from sshtunnel import SSHTunnelForwarder
import pymysql
import os

with SSHTunnelForwarder(
    (os.environ.get('SSH_HOST')),
    ssh_username=os.environ.get('ssh_username'),
    ssh_pkey="/Users/stefanfeiler/Desktop/SMARTBETTOR_CODEBASE/SmartBetter-website/test_kp.pem",
    remote_bind_address=(os.environ.get('database_endpoint'), 3306)
) as tunnel:
    print("****SSH Tunnel Established****")

    db = pymysql.connect(
        host='127.0.0.1', user="admin",
        password=os.environ.get('mysql_pass'), port=tunnel.local_bind_port
    )

    try:
        # Copy table 'placed_bets' from 'Micah' database to 'Stefan' database
        table_to_copy = 'login_info'
        with db.cursor() as cur:
            cur.execute('USE Micah')
            cur.execute(f'DESCRIBE {table_to_copy}')
            table_schema = cur.fetchall()
            cur.execute('USE Stefan')
            create_table_query = f'CREATE TABLE IF NOT EXISTS {table_to_copy} ('
            for column_info in table_schema:
                create_table_query += f'{column_info[0]} {column_info[1]} NOT NULL,'
            create_table_query = create_table_query[:-1] + ')'
            cur.execute(create_table_query)
            copy_data_query = f'INSERT INTO Stefan.{table_to_copy} SELECT * FROM Micah.{table_to_copy}'
            cur.execute(copy_data_query)
            db.commit()
            print("Table 'placed_bets' successfully copied from 'Micah' to 'Stefan' database.")
    finally:
        db.close()

print("YAYY!!")