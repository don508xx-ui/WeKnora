
import psycopg2
from psycopg2.extras import RealDictCursor
import json

print("=== Checking models schema ===")

conn = psycopg2.connect(
    host="124.156.200.84",
    port="32530",
    user="zeabur_user",
    password="ZkO1xpqj4H95U7L6R3JSbKgF2WC8XI0u",
    dbname="zeabur_db",
    sslmode="disable"
)

cur = conn.cursor()
cur.execute("""
    SELECT column_name, data_type
    FROM information_schema.columns
    WHERE table_name = 'models'
    ORDER BY ordinal_position
""")
cols = cur.fetchall()
for c in cols:
    print("  " + str(c))

print("\n--- Models data ---")
cur2 = conn.cursor(cursor_factory=RealDictCursor)
cur2.execute("SELECT * FROM models WHERE deleted_at IS NULL")
for m in cur2.fetchall():
    print("\nModel: " + str(m['name']))
    print("  Full data: " + str(m))

cur.close()
cur2.close()
conn.close()

