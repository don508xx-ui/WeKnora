
import psycopg2
from psycopg2.extras import RealDictCursor

print("=== Fixing deleted status ===\n")

# 旧数据库（正确的状态）
old_conn = psycopg2.connect(
    host="124.156.200.84",
    port="30815",
    user="root",
    password="ln6RtXI590Sva2pNomAc7O1T4BPi38Ew",
    dbname="zeabur",
    sslmode="disable"
)

old_cur = old_conn.cursor(cursor_factory=RealDictCursor)
old_cur.execute("SELECT id, title, deleted_at FROM knowledges")
old_rows = old_cur.fetchall()
old_cur.close()
old_conn.close()

print("Old DB knowledges status:")
deleted_ids_old = []
for r in old_rows:
    print("  " + str(r['title']) + " - deleted_at: " + str(r['deleted_at']))
    if r['deleted_at'] is not None:
        deleted_ids_old.append(r['id'])

print("\nFound " + str(len(deleted_ids_old)) + " deleted knowledges in old DB")

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

if len(deleted_ids_old) > 0:
    print("\nRestoring deleted_at in new DB...")
    placeholders = ','.join(['%s'] * len(deleted_ids_old))
    new_cur.execute("""
        UPDATE knowledges 
        SET deleted_at = NOW(), 
            parse_status = 'deleting',
            enable_status = 'disabled'
        WHERE id IN (%s)
    """ % placeholders, tuple(deleted_ids_old))
    print("Updated " + str(new_cur.rowcount) + " knowledges")

# 同时恢复旧数据库里 chunks 的 deleted_at
print("\nChecking old DB chunks deleted_at...")
old_conn2 = psycopg2.connect(
    host="124.156.200.84",
    port="30815",
    user="root",
    password="ln6RtXI590Sva2pNomAc7O1T4BPi38Ew",
    dbname="zeabur",
    sslmode="disable"
)
old_cur2 = old_conn2.cursor()
old_cur2.execute("SELECT id FROM chunks WHERE deleted_at IS NOT NULL")
old_deleted_chunks = [r[0] for r in old_cur2.fetchall()]
old_cur2.close()
old_conn2.close()

print("Found " + str(len(old_deleted_chunks)) + " deleted chunks in old DB")

if len(old_deleted_chunks) > 0:
    placeholders2 = ','.join(['%s'] * len(old_deleted_chunks))
    new_cur.execute("""
        UPDATE chunks 
        SET deleted_at = NOW()
        WHERE id IN (%s)
    """ % placeholders2, tuple(old_deleted_chunks))
    print("Updated " + str(new_cur.rowcount) + " chunks")

new_conn.commit()
new_cur.close()
new_conn.close()

print("\nDone! Refresh the browser.")

