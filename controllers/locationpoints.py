import pyodbc
from db import Conn
from controllers.auth import verify


def _rows(cur):
    cols = [c[0] for c in cur.description] if cur.description else []
    return [dict(zip(cols, r)) for r in cur.fetchall()] if cols else []


def list_points(trailid=None):
    try:
        cur = Conn.cursor()
        if trailid:
            cur.execute(
                'SELECT PointID, TrailID, Latitude, Longitude, Altitude FROM [dbo]."CW2.LOCATIONPOINT" WHERE TrailID = ?',
                trailid,
            )
        else:
            cur.execute(
                'SELECT PointID, TrailID, Latitude, Longitude, Altitude FROM [dbo]."CW2.LOCATIONPOINT"'
            )
        data = _rows(cur)
        cur.close()
        return data, 200
    except pyodbc.Error as e:
        return {"error": str(e)}, 400


def get_point(pointid):
    try:
        cur = Conn.cursor()
        cur.execute(
            'SELECT PointID, TrailID, Latitude, Longitude, Altitude FROM [dbo]."CW2.LOCATIONPOINT" WHERE PointID = ?',
            pointid,
        )
        data = _rows(cur)
        cur.close()
        return (data[0] if data else {}), 200
    except pyodbc.Error as e:
        return {"error": str(e)}, 400


def create_point(body):
    ok, res = verify()
    if not ok:
        return res
    try:
        cur = Conn.cursor()
        cur.execute(
            'INSERT INTO [dbo]."CW2.LOCATIONPOINT" (PointID, TrailID, Latitude, Longitude, Altitude) VALUES (?, ?, ?, ?, ?)',
            body["pointid"],
            body["trailid"],
            body.get("latitude"),
            body.get("longitude"),
            body.get("altitude"),
        )
        Conn.commit()
        cur.execute(
            'SELECT PointID, TrailID, Latitude, Longitude, Altitude FROM [dbo]."CW2.LOCATIONPOINT" WHERE PointID = ?',
            body["pointid"],
        )
        data = _rows(cur)
        cur.close()
        return (data[0] if data else {}), 201
    except pyodbc.Error as e:
        return {"error": str(e)}, 400


def update_point(pointid, body):
    ok, res = verify()
    if not ok:
        return res
    try:
        fields = []
        params = []
        for k, col in [
            ("trailid", "TrailID"),
            ("latitude", "Latitude"),
            ("longitude", "Longitude"),
            ("altitude", "Altitude"),
        ]:
            if k in body:
                fields.append(f"{col} = ?")
                params.append(body[k])
        if not fields:
            return {}, 200
        params.append(pointid)
        cur = Conn.cursor()
        cur.execute(
            'UPDATE [dbo]."CW2.LOCATIONPOINT" SET '
            + ", ".join(fields)
            + " WHERE PointID = ?",
            *params,
        )
        Conn.commit()
        cur.execute(
            'SELECT PointID, TrailID, Latitude, Longitude, Altitude FROM [dbo]."CW2.LOCATIONPOINT" WHERE PointID = ?',
            pointid,
        )
        data = _rows(cur)
        cur.close()
        return (data[0] if data else {}), 200
    except pyodbc.Error as e:
        return {"error": str(e)}, 400


def delete_point(pointid):
    ok, res = verify()
    if not ok:
        return res
    try:
        cur = Conn.cursor()
        cur.execute('DELETE FROM [dbo]."CW2.LOCATIONPOINT" WHERE PointID = ?', pointid)
        Conn.commit()
        cur.close()
        return "", 204
    except pyodbc.Error as e:
        return {"error": str(e)}, 400
