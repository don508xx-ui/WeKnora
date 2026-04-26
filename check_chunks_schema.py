
import psycopg2

print("=== Checking chunks schema ===")

# 旧数据库
old_conn = psycopg2.connect(
    host="124.156.200.84",
    port="30815",
    user="root",
    password="ln6RtXI590Sva2pNomAc7O1T4BPi38Ew",
    dbname="zeabur",
    sslmode="disable"
)

old_cur = old_conn.cursor()
old_cur.execute("""
    SELECT column_name, data_type, is_nullable
    FROM information_schema.columns
    WHERE table_name = 'chunks'
    ORDER BY ordinal_position
""")
old_cols = old_cur.fetchall()
old_cur.close()
old_conn.close()

print("\n--- Old DB ---")
for c in old_cols:
    print("  " + str(c))

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
new_cur.execute("""
    SELECT column_name, data_type, is_nullable
    FROM information_schema.columns
    WHERE table_name = 'chunks'
    ORDER BY ordinal_position
""")
new_cols = new_cur.fetchall()
new_cur.close()
new_conn.close()

print("\n--- New DB ---")
for c in new_cols:
    print("  " + str(c))

