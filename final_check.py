
import psycopg2

print("=== New DB Final Check ===\n")

conn = psycopg2.connect(
    host="124.156.200.84",
    port="32530",
    user="zeabur_user",
    password="ZkO1xpqj4H95U7L6R3JSbKgF2WC8XI0u",
    dbname="zeabur_db",
    sslmode="disable"
)

cur = conn.cursor()

# 检查扩展
print("Extensions:")
cur.execute("SELECT extname FROM pg_extension ORDER BY extname")
for row in cur.fetchall():
    print("  - " + row[0])

print("\n=== Table Counts ===")
tables = [
    'tenants', 'organizations', 'users', 'models',
    'knowledge_bases', 'knowledges', 'chunks',
    'sessions', 'messages', 'custom_agents', 'auth_tokens'
]

for table in tables:
    try:
        cur.execute("SELECT COUNT(*) FROM " + table)
        cnt = cur.fetchone()[0]
        print(table + ": " + str(cnt))
    except Exception as e:
        print(table + ": ERROR - " + str(e))

cur.close()
conn.close()

print("\n=== Done ===\n")
print("Now refresh the web app!")

