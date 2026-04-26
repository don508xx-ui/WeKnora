
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

print("=== New DB Status ===\n")

tables = ['tenants', 'users', 'models', 'knowledge_bases', 'knowledges', 'chunks']

for table in tables:
    try:
        cur.execute("SELECT COUNT(*) FROM " + table)
        cnt = cur.fetchone()[0]
        print(table + " = " + str(cnt))
    except Exception as e:
        print(table + " ERROR: " + str(e))

cur.close()
conn.close()

print("\nDone")

