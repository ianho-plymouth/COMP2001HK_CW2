import pyodbc
from db import Conn


def _rows(cur):
    cols = [c[0] for c in cur.description] if cur.description else []
    return [dict(zip(cols, r)) for r in cur.fetchall()] if cols else []


def create_user(body):
    try:
        cur = Conn.cursor()
        cur.execute(
            'EXEC dbo."CW2.UserCreate" ?, ?, ?',
            body["name"],
            body["email"],
            body["password"],
        )
        data = _rows(cur)
        Conn.commit()
        cur.close()
        return (data[0] if data else {}), 201
    except pyodbc.Error as e:
        return {"error": str(e)}, 400


def get_user(email):
    try:
        cur = Conn.cursor()
        cur.execute('EXEC dbo."CW2.UserRead" ?', email)
        data = _rows(cur)
        cur.close()
        return (data[0] if data else {}), 200
    except pyodbc.Error as e:
        return {"error": str(e)}, 400


def update_user(email, body):
    try:
        cur = Conn.cursor()
        name = body["name"]
        password = body["password"]
        cur.execute('EXEC dbo."CW2.UserUpdate" ?, ?, ?', name, email, password)
        data = _rows(cur)
        Conn.commit()
        cur.close()
        return (data[0] if data else {}), 200
    except pyodbc.Error as e:
        return {"error": str(e)}, 400


def delete_user(email):
    try:
        cur = Conn.cursor()
        cur.execute('EXEC dbo."CW2.UserDelete" ?', email)
        Conn.commit()
        cur.close()
        return "", 204
    except pyodbc.Error as e:
        return {"error": str(e)}, 400
