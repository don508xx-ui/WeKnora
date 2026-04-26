
import psycopg2
from psycopg2.extras import RealDictCursor

print("=== Checking knowledges full schema ===\n")

conn = psycopg2.connect(
    host="124.156.200.84",
    port="30815",
    user="root",
    password="ln6RtXI590Sva2pNomAc7O1T4BPi38Ew",
    dbname="zeabur",
    sslmode="disable"
)

cur = conn.cursor()
cur.execute("""
    SELECT column_name, data_type
    FROM information_schema.columns
    WHERE table_name = 'knowledges'
    ORDER BY ordinal_position
""")
cols = cur.fetchall()
for c in cols:
    print("  " + str(c))

print("\n--- Full row for kept knowledge ---")
cur2 = conn.cursor(cursor_factory=RealDictCursor)
cur2.execute("SELECT * FROM knowledges WHERE id = 'b6253b90-7dac-480b-8272-a400dfaaf4b4'")
row = cur2.fetchone()
for k, v in row.items():
    print("  " + k + ": " + str(v))

cur.close()
cur2.close()
conn.close()

