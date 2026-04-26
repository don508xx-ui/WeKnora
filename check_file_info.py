
import psycopg2
from psycopg2.extras import RealDictCursor

print("=== Checking knowledges file info ===\n")

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
old_cur.execute("SELECT id, title, file_info FROM knowledges WHERE id = 'b6253b90-7dac-480b-8272-a400dfaaf4b4'")
old_row = old_cur.fetchone()
old_cur.close()
old_conn.close()

print("Old DB file_info:")
print(old_row['file_info'])

# 新数据库
new_conn = psycopg2.connect(
    host="124.156.200.84",
    port="32530",
    user="zeabur_user",
    password="ZkO1xpqj4H95U7L6R3JSbKgF2WC8XI0u",
    dbname="zeabur_db",
    sslmode="disable"
)

new_cur = new_conn.cursor(cursor_factory=RealDictCursor)
new_cur.execute("SELECT id, title, file_info FROM knowledges WHERE id = 'b6253b90-7dac-480b-8272-a400dfaaf4b4'")
new_row = new_cur.fetchone()
new_cur.close()
new_conn.close()

print("\nNew DB file_info:")
print(new_row['file_info'])

