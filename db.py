import pyodbc

server = 'dist-6-505.uopnet.plymouth.ac.uk'
database = 'COMP2001_HK_CHo'
username = 'HK_CHo'
password = 'k6ZyLUY9'
driver = '{ODBC Driver 18 for SQL Server}'

conn_str = (
    f'DRIVER={driver};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password};'
    'Encrypt=Yes;'
    'TrustServerCertificate=Yes;'
    'Connection Timeout=30;'
    'Trusted_Connection=No;'
)

Conn = pyodbc.connect(conn_str)

if __name__ == "__main__":
    import pyodbc
    try:
        cur = Conn.cursor()
        cur.execute("SELECT @@VERSION AS version, DB_NAME() AS db, SYSTEM_USER AS [user]")
        row = cur.fetchone()
        print("Connection successful!")
        print("SQL Server Version：", row.version)
        print("Database：", row.db)
        print("User ID：", row.user)
    except pyodbc.Error as e:
        print("Connection Failed：", e)
