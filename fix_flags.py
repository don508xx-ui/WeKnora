
import psycopg2
from psycopg2.extras import RealDictCursor

print("Checking flags...\n")

conn = psycopg2.connect(
    host="124.156.200.84",
    port="32530",
    user="zeabur_user",
    password="ZkO1xpqj4H95U7L6R3JSbKgF2WC8XI0u",
    dbname="zeabur_db",
    sslmode="disable"
)

cur = conn.cursor()

# 先检查 chunks 表里的 flags 值
cur.execute("SELECT id, flags FROM chunks LIMIT 10")
rows = cur.fetchall()

print("Current flags values:")
for r in rows:
    print("  id: " + str(r[0]) + ", flags: " + str(r[1]))

print("\nChecking if flags can be NULL...")

# 尝试把 flags 都更新为0（默认值）
cur.execute("UPDATE chunks SET flags = 0 WHERE flags IS NULL")
conn.commit()
print("Updated " + str(cur.rowcount) + " rows")

cur.close()
conn.close()

print("\nDone! Now refresh the app!")

