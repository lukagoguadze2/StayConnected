import mysql.connector
from mysql.connector import Error
import os 

MYSQL_HOST = os.getenv('MYSQL_HOST') 
MYSQL_PORT = int(os.getenv('MYSQL_PORT'))  
MYSQL_USER = os.getenv('MYSQL_ROOT_USER') 
MYSQL_PASSWORD = os.getenv('MYSQL_ROOT_PASSWORD') 
DATABASES = os.getenv('DATABASES').split(',')  


def check_mysql_connection():
    try:
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD
        )
        
        if connection.is_connected():
            return True
        else:
            return False
    except Error as e:
        return False

def check_databases():
    try:
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD
        )
        
        cursor = connection.cursor()
        cursor.execute("SHOW DATABASES;")
        existing_databases = [db[0] for db in cursor.fetchall()]
        
        missing_databases = [db for db in DATABASES if db not in existing_databases]
        
        if missing_databases:
            return False
        else:
            return True
    except Error as e:
        return False
    finally:
        if connection.is_connected():
            connection.close()

if __name__ == "__main__":
    mysql_running = check_mysql_connection()
    if mysql_running:
        dbs_exist = check_databases()
        if dbs_exist:
            print(str(True).lower())
        else:
            print(str(False).lower())

    else:
        print(str(False).lower())
