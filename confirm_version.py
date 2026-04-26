
import psycopg2

conn = psycopg2.connect(
    host="124.156.200.84",
    port="32530",
    user="zeabur_user",
    password="ZkO1xpqj4H95U7L6R3JSbKgF2WC8XI0u",
    dbname="zeabur_db",
    sslmode="disable"
)

cur = conn.cursor()
cur.execute("SELECT version, dirty FROM schema_migrations")
ver, dirty = cur.fetchone()
cur.close()
conn.close()

print("New DB schema version: " + str(ver) + ", dirty: " + str(dirty))

