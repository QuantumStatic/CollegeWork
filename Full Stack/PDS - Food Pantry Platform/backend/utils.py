import pymysql
from dotenv import load_dotenv
import os

load_dotenv()
host = os.getenv('HOST')
user = os.getenv('USER')
password = os.getenv('PASSWORD')
db_name = os.getenv('DB_NAME')

def get_db_connection():
    try:
        connection = pymysql.connect(
            host = host,
            user = 'root',
            password = password,
            database = db_name,
            cursorclass = pymysql.cursors.DictCursor
        )
        return connection
    except:
        return False