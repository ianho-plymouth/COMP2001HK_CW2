import pyodbc
from db import Conn


def trail_summary_view():
    try:
        cur = Conn.cursor()
        cur.execute(
            'SELECT TrailID, TrailName, Description, Distance, ElevationGain, Difficulty, RouteType, EstimatedTime, IsPublic, LocationPointsCount FROM [dbo]."CW2.vTrailSummary"'
        )
        cols = [c[0] for c in cur.description] if cur.description else []
        data = [dict(zip(cols, r)) for r in cur.fetchall()] if cols else []
        cur.close()
        return data, 200
    except pyodbc.Error as e:
        return {"error": str(e)}, 400
