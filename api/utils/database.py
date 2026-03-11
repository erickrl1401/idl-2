import pymysql
import pymysql.cursors
from api.config import Config


def get_connection():
    """Return a new MySQL connection using PyMySQL."""
    return pymysql.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False,
    )


def execute_query(sql, params=None, fetch_one=False, fetch_all=False, commit=False):
    """
    Helper para ejecutar consultas SQL.

    Returns:
        - list[dict] si fetch_all=True
        - dict | None si fetch_one=True
        - int (lastrowid) si commit=True y es INSERT
        - None en caso contrario
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, params or ())
            if fetch_all:
                return cursor.fetchall()
            if fetch_one:
                return cursor.fetchone()
            if commit:
                conn.commit()
                return cursor.lastrowid
            conn.commit()
            return None
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
