import trino

conn = trino.dbapi.connect(
    host='localhost',
    port="8080",
    user="<username>",
    catalog="chinook_database",
    schema="public")

run = conn.cursor().execute("SELECT * FROM chinook_database.public.album LIMIT 5")
rows = run.fetchall()
for row in rows:
    print(row)
