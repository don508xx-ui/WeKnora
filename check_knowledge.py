
import psycopg2
from psycopg2.extras import RealDictCursor

print("Checking knowledges and knowledge_bases...\n")

conn = psycopg2.connect(
    host="124.156.200.84",
    port="32530",
    user="zeabur_user",
    password="ZkO1xpqj4H95U7L6R3JSbKgF2WC8XI0u",
    dbname="zeabur_db",
    sslmode="disable"
)

cur = conn.cursor(cursor_factory=RealDictCursor)

print("=== knowledge_bases ===")
cur.execute("SELECT id, name, tenant_id FROM knowledge_bases")
for row in cur.fetchall():
    print("id: " + str(row['id']))
    print("name: " + str(row['name']))
    print("tenant_id: " + str(row['tenant_id']) + "\n")

print("=== knowledges ===")
cur.execute("SELECT id, title, knowledge_base_id, tenant_id FROM knowledges")
for row in cur.fetchall():
    print("id: " + str(row['id']))
    print("title: " + str(row['title']))
    print("kb_id: " + str(row['knowledge_base_id']))
    print("tenant_id: " + str(row['tenant_id']) + "\n")

cur.close()
conn.close()

