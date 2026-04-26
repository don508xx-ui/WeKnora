
import psycopg2
from psycopg2.extras import RealDictCursor
import json

print("Connecting...")

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

print("Reading models from old DB...")
old_cur = old_conn.cursor(cursor_factory=RealDictCursor)
old_cur.execute("SELECT * FROM models")
models = old_cur.fetchall()
old_cur.close()
print("Found " + str(len(models)) + " models")

print("Clearing new DB models...")
new_cur = new_conn.cursor()
new_cur.execute("DELETE FROM models")
new_conn.commit()
new_cur.close()

print("Inserting into new DB...")
new_cur = new_conn.cursor()

count = 0
for m in models:
    cols = list(m.keys())
    vals = []
    for v in m.values():
        if isinstance(v, dict):
            vals.append(json.dumps(v))
        else:
            vals.append(v)
    placeholders = ','.join(['%s'] * len(vals))
    sql = "INSERT INTO models (" + ','.join(cols) + ") VALUES (" + placeholders + ")"
    new_cur.execute(sql, vals)
    count += 1

new_conn.commit()
new_cur.close()

old_conn.close()
new_conn.close()

print("Done! Copied " + str(count) + " models")

