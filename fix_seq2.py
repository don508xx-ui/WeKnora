
import psycopg2

print("=== Fixing chunks_seq_id_seq ===\n")

conn = psycopg2.connect(
    host="124.156.200.84",
    port="32530",
    user="zeabur_user",
    password="ZkO1xpqj4H95U7L6R3JSbKgF2WC8XI0u",
    dbname="zeabur_db",
    sslmode="disable"
)

cur = conn.cursor()

cur.execute("SELECT COALESCE(MAX(seq_id), 0) FROM chunks")
max_seq = cur.fetchone()[0]
print("Max seq_id: " + str(max_seq))

print("\nResetting chunks_seq_id_seq to " + str(max_seq + 1))
cur.execute("SELECT setval('chunks_seq_id_seq', %s, true)", (max_seq + 1,))

conn.commit()
cur.close()
conn.close()

print("\nDone! Try uploading again!")

