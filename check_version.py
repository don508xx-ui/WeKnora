
import psycopg2

print("=== Checking schema versions ===\n")

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
old_cur.execute("SELECT version, dirty FROM schema_migrations")
old_ver, old_dirty = old_cur.fetchone()
old_cur.close()
old_conn.close()

print("Old DB (port 30815):")
print("  version: " + str(old_ver))
print("  dirty: " + str(old_dirty))

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
new_cur.close()
new_conn.close()

print("\nNew DB (port 32530):")
print("  version: " + str(new_ver))
print("  dirty: " + str(new_dirty))

print("\n---")
if old_ver != new_ver:
    print("\nMISMATCH! Updating new DB version...")
    new_conn2 = psycopg2.connect(
        host="124.156.200.84",
        port="32530",
        user="zeabur_user",
        password="ZkO1xpqj4H95U7L6R3JSbKgF2WC8XI0u",
        dbname="zeabur_db",
        sslmode="disable"
    )
    new_cur2 = new_conn2.cursor()
    new_cur2.execute("UPDATE schema_migrations SET version = %s, dirty = %s", (old_ver, old_dirty))
    new_conn2.commit()
    new_cur2.close()
    new_conn2.close()
    print("Updated to version " + str(old_ver))
else:
    print("\nVersions match!")

