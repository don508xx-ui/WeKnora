
import psycopg2
from psycopg2.extras import RealDictCursor

print("Checking knowledges parse_status...\n")

conn = psycopg2.connect(
    host="124.156.200.84",
    port="32530",
    user="zeabur_user",
    password="ZkO1xpqj4H95U7L6R3JSbKgF2WC8XI0u",
    dbname="zeabur_db",
    sslmode="disable"
)

cur = conn.cursor(cursor_factory=RealDictCursor)
cur.execute("SELECT id, title, parse_status, enable_status FROM knowledges")

for row in cur.fetchall():
    print("Title: " + str(row['title']))
    print("  parse_status: " + str(row['parse_status']))
    print("  enable_status: " + str(row['enable_status']))
    print("")

cur.close()
conn.close()

print("\nChecking if any chunks have deleted_at set...")

conn2 = psycopg2.connect(
    host="124.156.200.84",
    port="32530",
    user="zeabur_user",
    password="ZkO1xpqj4H95U7L6R3JSbKgF2WC8XI0u",
    dbname="zeabur_db",
    sslmode="disable"
)

cur2 = conn2.cursor()
cur2.execute("SELECT COUNT(*) FROM chunks WHERE deleted_at IS NOT NULL")
deleted_chunks = cur2.fetchone()[0]

print("Deleted chunks: " + str(deleted_chunks))

cur2.close()
conn2.close()

