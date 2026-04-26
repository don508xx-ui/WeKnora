
import psycopg2
from psycopg2.extras import RealDictCursor
import json

print("=== Syncing full knowledges row ===\n")

# 旧数据库
old_conn = psycopg2.connect(
    host="124.156.200.84",
    port="30815",
    user="root",
    password="ln6RtXI590Sva2pNomAc7O1T4BPi38Ew",
    dbname="zeabur",
    sslmode="disable"
)

old_cur = old_conn.cursor(cursor_factory=RealDictCursor)
old_cur.execute("SELECT * FROM knowledges WHERE id = 'b6253b90-7dac-480b-8272-a400dfaaf4b4'")
old_row = old_cur.fetchone()
old_cur.close()
old_conn.close()

# 新数据库
new_conn = psycopg2.connect(
    host="124.156.200.84",
    port="32530",
    user="zeabur_user",
    password="ZkO1xpqj4H95U7L6R3JSbKgF2WC8XI0u",
    dbname="zeabur_db",
    sslmode="disable"
)

new_cur = new_conn.cursor()

# 构建UPDATE语句
set_parts = []
values = []
for k, v in old_row.items():
    if k == 'id':
        continue
    set_parts.append(f"{k} = %s")
    if isinstance(v, dict):
        values.append(json.dumps(v))
    else:
        values.append(v)

values.append(old_row['id'])

sql = f"UPDATE knowledges SET " + ", ".join(set_parts) + " WHERE id = %s"

print("Updating...")
new_cur.execute(sql, tuple(values))
new_conn.commit()

print("Updated " + str(new_cur.rowcount) + " rows")

new_cur.close()
new_conn.close()

print("\nDone! Refresh the browser!")

