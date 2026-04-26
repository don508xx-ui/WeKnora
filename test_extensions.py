
import psycopg2
from psycopg2.extras import RealDictCursor

print("=== Testing New DB Extensions ===\n")

conn = psycopg2.connect(
    host="124.156.200.84",
    port="32530",
    user="zeabur_user",
    password="ZkO1xpqj4H95U7L6R3JSbKgF2WC8XI0u",
    dbname="zeabur_db",
    sslmode="disable"
)

cur = conn.cursor()

# 1. 检查已安装扩展
print("1. Installed Extensions:")
cur.execute("SELECT extname FROM pg_extension ORDER BY extname")
for row in cur.fetchall():
    print("   - " + row[0])

# 2. 测试 pg_trgm 关键词搜索
print("\n2. Testing pg_trgm search:")
try:
    cur.execute("""
        SELECT id, content, 1 - (content <-> '星座') as score
        FROM chunks
        WHERE deleted_at IS NULL
        ORDER BY score DESC
        LIMIT 3
    """)
    results = cur.fetchall()
    print("   Found " + str(len(results)) + " results:")
    for r in results:
        print("   Score: " + str(r[2]) + " - " + str(r[1])[:60] + "...")
except Exception as e:
    print("   Error: " + str(e))

# 3. 检查 chunks 表是否有 embedding 数据
print("\n3. Checking chunks and embeddings:")
cur.execute("SELECT COUNT(*) FROM chunks WHERE deleted_at IS NULL")
print("   Active chunks: " + str(cur.fetchone()[0]))

cur.execute("SELECT COUNT(*) FROM embeddings")
print("   Embeddings: " + str(cur.fetchone()[0]))

# 4. 测试 pgvector 是否能用
print("\n4. Testing pgvector basic:")
try:
    # 先检查有没有向量数据
    cur.execute("SELECT COUNT(*) FROM embeddings WHERE embedding IS NOT NULL")
    count = cur.fetchone()[0]
    print("   Embeddings with vector: " + str(count))
except Exception as e:
    print("   Error: " + str(e))

cur.close()
conn.close()

print("\n=== Test Complete ===")

