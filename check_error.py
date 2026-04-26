
import psycopg2
from psycopg2.extras import RealDictCursor

print("=== Checking knowledges error messages ===\n")

conn = psycopg2.connect(
    host="124.156.200.84",
    port="32530",
    user="zeabur_user",
    password="ZkO1xpqj4H95U7L6R3JSbKgF2WC8XI0u",
    dbname="zeabur_db",
    sslmode="disable"
)

cur = conn.cursor(cursor_factory=RealDictCursor)
cur.execute("SELECT id, title, parse_status, error_message FROM knowledges WHERE deleted_at IS NULL")
rows = cur.fetchall()

for row in rows:
    print("Title: " + str(row['title']))
    print("  parse_status: " + str(row['parse_status']))
    print("  error_message: " + str(row['error_message']) + "\n")

cur.close()
conn.close()

