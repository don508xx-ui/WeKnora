
import psycopg2

print("=== Fixing seq_id sequence ===\n")

conn = psycopg2.connect(
    host="124.156.200.84",
    port="32530",
    user="zeabur_user",
    password="ZkO1xpqj4H95U7L6R3JSbKgF2WC8XI0u",
    dbname="zeabur_db",
    sslmode="disable"
)

cur = conn.cursor()

# 1. 检查 chunks 表的最大 seq_id
cur.execute("SELECT COALESCE(MAX(seq_id), 0) FROM chunks")
max_seq = cur.fetchone()[0]
print("Current max seq_id: " + str(max_seq))

# 2. 查找 seq_id 相关的序列
print("\nLooking for sequences...")
cur.execute("""
    SELECT sequence_name 
    FROM information_schema.sequences 
    WHERE sequence_schema = 'public'
""")
seqs = cur.fetchall()
for s in seqs:
    print("  " + s[0])

# 3. 如果找到序列，重置它
if len(seqs) > 0:
    seq_name = seqs[0][0]
    print("\nResetting sequence " + seq_name + " to " + str(max_seq + 1))
    cur.execute(f"SELECT setval('{seq_name}', {max_seq + 1}, true)")

# 另外，检查一下 chunks 表的结构，看看 seq_id 是不是自增的
print("\nChecking chunks seq_id column...")
cur.execute("""
    SELECT column_name, column_default
    FROM information_schema.columns
    WHERE table_name = 'chunks' AND column_name = 'seq_id'
""")
col_info = cur.fetchone()
print("  " + str(col_info))

conn.commit()
cur.close()
conn.close()

print("\nDone! Now try re-uploading the documents.")

