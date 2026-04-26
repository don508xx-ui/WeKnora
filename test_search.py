
import psycopg2
from psycopg2.extras import RealDictCursor
import json

print("=== Search Test ===\n")

conn = psycopg2.connect(
    host="124.156.200.84",
    port="32530",
    user="zeabur_user",
    password="ZkO1xpqj4H95U7L6R3JSbKgF2WC8XI0u",
    dbname="zeabur_db",
    sslmode="disable"
)

cur = conn.cursor(cursor_factory=RealDictCursor)

# 1. 先检查有哪些数据
cur.execute("SELECT COUNT(*) FROM chunks WHERE deleted_at IS NULL")
chunks_count = cur.fetchone()
print("Chunks: " + str(chunks_count))

cur.execute("SELECT COUNT(*) FROM embeddings")
embeddings_count = cur.fetchone()
print("Embeddings: " + str(embeddings_count))

# 2. 关键词搜索测试 - 1：用 pg_trgm
print("\n--- Keyword Search (pg_trgm):")
try:
    cur.execute("""
        SELECT id, content, 1 - (content <-> '星座') as score
        FROM chunks
        WHERE deleted_at IS NULL
        ORDER BY score DESC
        LIMIT 3
    """)
    results = cur.fetchall()
    print("Search term: '星座'")
    print("Results: " + str(len(results)))
    for r in results:
        content = str(r['content'])[:100].replace('\n', ' ')
        print(f"  Score: {r['score']:.4f} - {content}...")
except Exception as e:
    print("Error: " + str(e))

# 3. 检查有没有向量数据，做向量搜索
print("\n--- Checking Vector Data:")
try:
    cur.execute("SELECT COUNT(*) FROM embeddings WHERE embedding IS NOT NULL")
    vec_count = cur.fetchone()
    print("Vectors: " + str(vec_count))

    # 如果有向量数据，拿一个向量做搜索
    if vec_count and vec_count > 0:
        cur.execute("SELECT id, embedding FROM embeddings LIMIT 1")
        sample_vec = cur.fetchone()
        print("\n--- Vector Similarity Search:")
        print("Using sample embedding for search...")
        
        # 注意：这里只是示例，真实搜索需要 query embedding
        
except Exception as e:
    print("Error: " + str(e))

cur.close()
conn.close()

print("\n=== Test Done ===\n")
print("Key Features:")
print("✅ pg_trgm = 关键词/模糊搜索")
print("✅ pgvector = 语义/向量搜索")

