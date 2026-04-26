
import psycopg2

print("=== Fixing Schema Version ===\n")

# 旧数据库（完整版本）
old_conn = psycopg2.connect(
    host="124.156.200.84",
    port="30815",
    user="root",
    password="ln6RtXI590Sva2pNomAc7O1T4BPi38Ew",
    dbname="zeabur",
    sslmode="disable"
)

old_cur = old_conn.cursor()
old_cur.execute("SELECT version, dirty FROM schema_migrations")
old_ver, old_dirty = old_cur.fetchone()
old_cur.close()
old_conn.close()

print("Old DB: version " + str(old_ver) + ", dirty: " + str(old_dirty))

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
new_cur.execute("SELECT version, dirty FROM schema_migrations")
new_ver, new_dirty = new_cur.fetchone()

print("\nNew DB: version " + str(new_ver) + ", dirty: " + str(new_dirty))

if old_ver != new_ver:
    print("\nUpdating schema_migrations in new DB...")
    new_cur.execute("UPDATE schema_migrations SET version = %s, dirty = %s", (old_ver, old_dirty))
    new_conn.commit()
    print("Updated to version " + str(old_ver))

new_cur.close()
new_conn.close()

print("\nDone! Now refresh the app!")

