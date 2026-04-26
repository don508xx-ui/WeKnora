
import psycopg2
from psycopg2.extras import RealDictCursor

print("=== Checking chunks data ===\n")

# 旧数据库
old_conn = psycopg2.connect(
    host="124.156.200.84",
    port="30815",
    user="root",
    password="ln6RtXI590Sva2pNomAc7O1T4BPi38Ew",
    dbname="zeabur",
    sslmode="disable"
)

# 新数据库
new_conn = psycopg2.connect(
    host="124.156.200.84",
    port="32530",
    user="zeabur_user",
    password="ZkO1xpqj4H95U7L6R3JSbKgF2WC8XI0u",
    dbname="zeabur_db",
    sslmode="disable"
)

print("Old DB (port 30815):")
old_cur = old_conn.cursor(cursor_factory=RealDictCursor)
old_cur.execute("SELECT id, knowledge_id, content FROM chunks LIMIT 3")
old_rows = old_cur.fetchall()
old_cur.close()
for r in old_rows:
    print("  id: " + r['id'])
    print("  knowledge_id: " + str(r['knowledge_id']))
    print("  content snippet: " + str(r['content'])[:50] + "...\n")

print("\nNew DB (port 32530):")
new_cur = new_conn.cursor(cursor_factory=RealDictCursor)
new_cur.execute("SELECT id, knowledge_id, content FROM chunks LIMIT 3")
new_rows = new_cur.fetchall()
new_cur.close()
for r in new_rows:
    print("  id: " + r['id'])
    print("  knowledge_id: " + str(r['knowledge_id']))
    print("  content snippet: " + str(r['content'])[:50] + "...\n")

old_conn.close()
new_conn.close()

print("Done checking")

