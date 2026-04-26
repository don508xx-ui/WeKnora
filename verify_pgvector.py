
import psycopg2

print("Checking new DB...")

conn = psycopg2.connect(
    host="124.156.200.84",
    port="32530",
    user="zeabur_user",
    password="ZkO1xpqj4H95U7L6R3JSbKgF2WC8XI0u",
    dbname="zeabur_db",
    sslmode="disable"
)

cur = conn.cursor()

print("\nExtensions:")
cur.execute("SELECT extname FROM pg_extension ORDER BY extname")
for row in cur.fetchall():
    print("  - " + row[0])

print("\nChecking if vector type exists:")
try:
    cur.execute("SELECT typname FROM pg_type WHERE typname = 'vector'")
    row = cur.fetchone()
    if row:
        print("  ✓ vector type exists!")
    else:
        print("  ✗ vector type not found")
except Exception as e:
    print("  Error: " + str(e))

cur.close()
conn.close()
print("\nDone!")

