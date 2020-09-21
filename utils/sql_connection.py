import psycopg2
from psycopg2 import pool
from contextlib import contextmanager
from config import Database



postgreSQL_pool = psycopg2.pool.SimpleConnectionPool(Database.min_connection, Database.max_connection,
                                              user = Database.user,
                                              password = Database.password,
                                              host = Database.host,
                                              port = Database.port,
                                              database = Database.database
                                              )


@contextmanager
def connection():
    global postgreSQL_pool
    conn = postgreSQL_pool.getconn()
    try:
        csr = conn.cursor()
        yield csr
    except Exception as e:
        print(e)
        conn.rollback()
    finally:
        csr.close()
        postgreSQL_pool.putconn(conn)
    