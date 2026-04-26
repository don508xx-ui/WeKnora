
import psycopg2

print("=== Restoring data ===\n")

conn = psycopg2.connect(
    host="124.156.200.84",
    port="32530",
    user="zeabur_user",
    password="ZkO1xpqj4H95U7L6R3JSbKgF2WC8XI0u",
    dbname="zeabur_db",
    sslmode="disable"
)

cur = conn.cursor()

print("1. Restoring chunks: clearing deleted_at...")
cur.execute("UPDATE chunks SET deleted_at = NULL")
print("   Updated " + str(cur.rowcount) + " chunks")

print("\n2. Restoring knowledges parse_status...")
cur.execute("""
    UPDATE knowledges 
    SET parse_status = 'processed', 
        enable_status = 'enabled',
        deleted_at = NULL
""")
print("   Updated " + str(cur.rowcount) + " knowledges")

conn.commit()
cur.close()
conn.close()

print("\nDone! Now refresh your browser! 🎉")

