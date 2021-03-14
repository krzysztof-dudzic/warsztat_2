from psycopg2 import connect, OperationalError
from psycopg2.errors import DuplicateDatabase


CREATE_DB = "CREATE DATABASE password_db;"
CREATE_USERS_TABLE = "CREATE TABLE users(" \
                     "id serial NOT NULL," \
                     "username varchar(255)," \
                     "hashed_password varchar(80)," \
                     "PRIMARY KEY (id));"

CREATE_MESSAGES = "CREATE TABLE messages(" \
                  "id serial NOT NULL," \
                  "from_id int REFERNCES users(id) ON DELETE CASCADE," \
                  "to_id int REFERENCES users(id) ON DELETE CASCADE," \
                  "text VARCHAR(255)," \
                  "creation_date TIMESTAMP default CURRENT_TIMESTAMP)"

DB_USER = "postgres"
PASSWORD = "coderslab"
HOST = "localhost"
try:
    con = connect(host=HOST, user=DB_USER, password=PASSWORD, database='workshop')
    con.autocommit = True

    cursor = con.cursor()

    try:
        cursor.execute(CREATE_DB)
        print("Database created successfully")
    except DuplicateDatabase as a:
        print("Database exists ", a)
    con.close()

except OperationalError as a:
    print("Connection errror: ", a)


try:
    con = connect(host=HOST, user=DB_USER, password=PASSWORD, database='workshop')
    con.autocommit = True

    cursor = con.cursor()
    try:
        cursor.execute(CREATE_USERS_TABLE)
        print("Table users created")
    except DuplicateDatabase as a:
        print("Table users exists ", a)

    try:
        cursor.execute(CREATE_MESSAGES)
        print("Table messages created")
    except DuplicateDatabase as a:
        print("Table messages exists: ", a)
    con.close()
except OperationalError as a:
    print("Connection Error: ", a)










