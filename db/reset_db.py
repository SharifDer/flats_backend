import psycopg2
from urllib.parse import urlparse
import os
from dotenv import load_dotenv

DATABASE_URL = os.getenv("DATABASE_URL")
INIT_SCHEMA_FILE = "db/init_schema.sql"

# Parse DB URL
parsed = urlparse(DATABASE_URL)
user = parsed.username
password = parsed.password
host = parsed.hostname
port = parsed.port or 5432
db_name = parsed.path.lstrip('/')

load_dotenv()
def drop_and_create_database():
    # Connect to default database (postgres)
    conn = psycopg2.connect(
        dbname="postgres",
        user=user,
        password=password,
        host=host,
        port=port
    )
    conn.autocommit = True
    cur = conn.cursor()

    # Drop and recreate database
    cur.execute(f"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = %s;", (db_name,))
    cur.execute(f"DROP DATABASE IF EXISTS {db_name};")
    cur.execute(f"CREATE DATABASE {db_name};")

    cur.close()
    conn.close()

def run_schema():
    # Connect to new database
    conn = psycopg2.connect(
        dbname=db_name,
        user=user,
        password=password,
        host=host,
        port=port
    )
    cur = conn.cursor()

    with open(INIT_SCHEMA_FILE, "r") as f:
        schema_sql = f.read()
        cur.execute(schema_sql)

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    drop_and_create_database()
    run_schema()
    print(f"Database '{db_name}' reset and initialized from '{INIT_SCHEMA_FILE}'")
