
import psycopg2
from psycopg2.extras import RealDictCursor

conn = psycopg2.connect(
    host="124.156.200.84",
    port="30815",
    user="root",
    password="ln6RtXI590Sva2pNomAc7O1T4BPi38Ew",
    dbname="zeabur",
    sslmode="disable"
)

cur = conn.cursor(cursor_factory=RealDictCursor)
cur.execute("SELECT id, title, deleted_at FROM knowledges")
print("Old DB knowledges:")
for row in cur.fetchall():
    print("  id: " + row['id'])
    print("  title: " + str(row['title']))
    print("  deleted_at: " + str(row['deleted_at']) + "\n")

cur.close()
conn.close()

