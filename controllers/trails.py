import pyodbc
from db import Conn
from controllers.auth import verify


def _rows(cur):
    cols = [c[0] for c in cur.description] if cur.description else []
    return [dict(zip(cols, r)) for r in cur.fetchall()] if cols else []


def list_trails():
    try:
        cur = Conn.cursor()
        cur.execute(
            'SELECT TrailID, TrailName, Description, Distance, ElevationGain, Difficulty, RouteType, EstimatedTime, IsPublic, UserID FROM [dbo]."CW2.TRAIL"'
        )
        data = _rows(cur)
        cur.close()
        return data, 200
    except pyodbc.Error as e:
        return {"error": str(e)}, 400


def get_trail(trailid):
    try:
        cur = Conn.cursor()
        cur.execute(
            'SELECT TrailID, TrailName, Description, Distance, ElevationGain, Difficulty, RouteType, EstimatedTime, IsPublic, UserID FROM [dbo]."CW2.TRAIL" WHERE TrailID = ?',
            trailid,
        )
        data = _rows(cur)
        cur.close()
        return (data[0] if data else {}), 200
    except pyodbc.Error as e:
        return {"error": str(e)}, 400


def create_trail(body):
    ok, res = verify()
    if not ok:
        return res
    try:
        cur = Conn.cursor()
        cur.execute(
            'INSERT INTO [dbo]."CW2.TRAIL" (TrailID, TrailName, Description, Distance, ElevationGain, Difficulty, RouteType, EstimatedTime, IsPublic, UserID) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            body["trailid"],
            body["trailname"],
            body.get("description"),
            int(body["distance"]),
            int(body["elevationgain"]),
            body["difficulty"],
            body["routetype"],
            body.get("estimatedtime"),
            int(body["ispublic"]),
            int(body["userid"]),
        )
        Conn.commit()
        cur.execute(
            'SELECT TrailID, TrailName, Description, Distance, ElevationGain, Difficulty, RouteType, EstimatedTime, IsPublic, UserID FROM [dbo]."CW2.TRAIL" WHERE TrailID = ?',
            body["trailid"],
        )
        data = _rows(cur)
        cur.close()
        return (data[0] if data else {}), 201
    except pyodbc.Error as e:
        return {"error": str(e)}, 400


def update_trail(trailid, body):
    ok, res = verify()
    if not ok:
        return res
    try:
        fields = []
        params = []
        for k, col in [
            ("trailname", "TrailName"),
            ("description", "Description"),
            ("distance", "Distance"),
            ("elevationgain", "ElevationGain"),
            ("difficulty", "Difficulty"),
            ("routetype", "RouteType"),
            ("estimatedtime", "EstimatedTime"),
            ("ispublic", "IsPublic"),
            ("userid", "UserID"),
        ]:
            if k in body:
                fields.append(f"{col} = ?")
                v = body[k]
                if (
                    k
                    in [
                        "distance",
                        "elevationgain",
                        "estimatedtime",
                        "ispublic",
                        "userid",
                    ]
                    and v is not None
                ):
                    v = int(v)
                params.append(v)
        if not fields:
            return {}, 200
        params.append(trailid)
        cur = Conn.cursor()
        cur.execute(
            'UPDATE [dbo]."CW2.TRAIL" SET ' + ", ".join(fields) + " WHERE TrailID = ?",
            *params,
        )
        Conn.commit()
        cur.execute(
            'SELECT TrailID, TrailName, Description, Distance, ElevationGain, Difficulty, RouteType, EstimatedTime, IsPublic, UserID FROM [dbo]."CW2.TRAIL" WHERE TrailID = ?',
            trailid,
        )
        data = _rows(cur)
        cur.close()
        return (data[0] if data else {}), 200
    except pyodbc.Error as e:
        return {"error": str(e)}, 400


def delete_trail(trailid):
    ok, res = verify()
    if not ok:
        return res
    try:
        cur = Conn.cursor()
        cur.execute('DELETE FROM [dbo]."CW2.TRAIL" WHERE TrailID = ?', trailid)
        Conn.commit()
        cur.close()
        return "", 204
    except pyodbc.Error as e:
        return {"error": str(e)}, 400


def public_summary():
    try:
        cur = Conn.cursor()
        cur.execute(
            'SELECT TrailID, TrailName, Description, Distance, ElevationGain, Difficulty, RouteType, EstimatedTime, IsPublic, LocationPointsCount FROM [dbo]."CW2.vTrailSummary"'
        )
        data = _rows(cur)
        cur.close()
        return data, 200
    except pyodbc.Error as e:
        return {"error": str(e)}, 400
