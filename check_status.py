
import psycopg2

print("Checking new DB tables...\n")

conn = psycopg2.connect(
    host="124.156.200.84",
    port="32530",
    user="zeabur_user",
    password="ZkO1xpqj4H95U7L6R3JSbKgF2WC8XI0u",
    dbname="zeabur_db",
    sslmode="disable"
)

cur = conn.cursor()

tables = [
    'tenants',
    'organizations',
    'users',
    'models',
    'knowledge_bases',
    'knowledges',
    'chunks',
    'sessions',
    'messages',
    'custom_agents'
]

for table in tables:
    try:
        cur.execute("SELECT COUNT(*) FROM " + table)
        count = cur.fetchone()[0]
        print(table + ": " + str(count) + " 行")
    except Exception as e:
        print(table + ": 错误 - " + str(e))

cur.close()
conn.close()
print("\nDone!")

