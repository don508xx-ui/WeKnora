
import psycopg2
from psycopg2.extras import RealDictCursor

print("=== Checking New Uploaded Documents ===\n")

conn = psycopg2.connect(
    host="124.156.200.84",
    port="32530",
    user="zeabur_user",
    password="ZkO1xpqj4H95U7L6R3JSbKgF2WC8XI0u",
    dbname="zeabur_db",
    sslmode="disable"
)

cur = conn.cursor(cursor_factory=RealDictCursor)

# 1. 检查 knowledges
cur.execute("SELECT id, title, parse_status FROM knowledges WHERE deleted_at IS NULL")
knowledges = cur.fetchall()
print("Active Knowledges (" + str(len(knowledges)) + "):")
for k in knowledges:
    print("  - " + str(k['title']) + " (" + str(k['parse_status']) + ")")

# 2. 检查 chunks
cur.execute("SELECT COUNT(*) FROM chunks WHERE deleted_at IS NULL")
chunks_count = cur.fetchone()[0]
print("\nActive Chunks: " + str(chunks_count))

# 3. 检查 embeddings
cur.execute("SELECT COUNT(*) FROM embeddings")
embeddings_count = cur.fetchone()[0]
print("Embeddings: " + str(embeddings_count))

# 4. 看看最近解析成功的文档
if len(knowledges) > 0:
    cur.execute("""
        SELECT c.id, c.content, c.knowledge_id
        FROM chunks c
        WHERE c.deleted_at IS NULL
        ORDER BY c.created_at DESC
        LIMIT 5
    """)
    recent_chunks = cur.fetchall()
    print("\nRecent Chunks (" + str(len(recent_chunks)) + "):")
    for i, c in enumerate(recent_chunks):
        content_preview = str(c['content'])[:80].replace('\n', ' ')
        print(f"  {i+1}. {content_preview}...")

cur.close()
conn.close()

print("\n=== Done checking ===")

