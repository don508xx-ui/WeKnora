
import psycopg2

print("=== Final fix: restoring deleted status ===\n")

# 新数据库
conn = psycopg2.connect(
    host="124.156.200.84",
    port="32530",
    user="zeabur_user",
    password="ZkO1xpqj4H95U7L6R3JSbKgF2WC8XI0u",
    dbname="zeabur_db",
    sslmode="disable"
)

cur = conn.cursor()

# 只有这个ID的文档是保留的，其他都删除
keep_id = "b6253b90-7dac-480b-8272-a400dfaaf4b4"

print("Marking knowledges as deleted except " + keep_id)
cur.execute("""
    UPDATE knowledges
    SET deleted_at = NOW(),
        parse_status = 'deleting',
        enable_status = 'disabled'
    WHERE id != %s
""", (keep_id,))
print("Updated " + str(cur.rowcount) + " knowledges")

print("\nMarking chunks as deleted except those linked to " + keep_id)
cur.execute("""
    UPDATE chunks
    SET deleted_at = NOW()
    WHERE knowledge_id != %s
""", (keep_id,))
print("Updated " + str(cur.rowcount) + " chunks")

print("\nRestoring the keep knowledge:")
cur.execute("""
    UPDATE knowledges
    SET deleted_at = NULL,
        parse_status = 'processed',
        enable_status = 'enabled'
    WHERE id = %s
""", (keep_id,))

cur.execute("""
    UPDATE chunks
    SET deleted_at = NULL
    WHERE knowledge_id = %s
""", (keep_id,))

conn.commit()
cur.close()
conn.close()

print("\nDone! Refresh the browser!")

