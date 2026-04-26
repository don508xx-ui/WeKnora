
import psycopg2

print("Checking chunks...\n")

# 新数据库
conn = psycopg2.connect(
    host="124.156.200.84",
    port="32530",
    user="zeabur_user",
    password="ZkO1xpqj4H95U7L6R3JSbKgF2WC8XI0u",
    dbname="zeabur_db",
    sslmode="disable"
)

cur = conn.cursor()

cur.execute("SELECT COUNT(*) FROM chunks")
cnt = cur.fetchone()[0]
print("Total chunks: " + str(cnt))

if cnt > 0:
    cur.execute("SELECT id, knowledge_id FROM chunks LIMIT 5")
    print("\nFirst 5 chunks:")
    for row in cur.fetchall():
        print("  id: " + str(row[0]) + ", knowledge_id: " + str(row[1]))

cur.close()
conn.close()

