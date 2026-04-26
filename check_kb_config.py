
import psycopg2
from psycopg2.extras import RealDictCursor
import json

print("=== Checking Knowledge Base Configuration ===\n")

conn = psycopg2.connect(
    host="124.156.200.84",
    port="32530",
    user="zeabur_user",
    password="ZkO1xpqj4H95U7L6R3JSbKgF2WC8XI0u",
    dbname="zeabur_db",
    sslmode="disable"
)

cur = conn.cursor(cursor_factory=RealDictCursor)
cur.execute("SELECT * FROM knowledge_bases WHERE deleted_at IS NULL")
kb = cur.fetchone()

print("Knowledge Base: " + str(kb['name']))
print("Full config: " + str(kb))

# 检查有没有配置默认 embedding 模型
print("\n--- Embedding Models ---")
cur.execute("""
    SELECT id, name, is_default 
    FROM models 
    WHERE type = 'Embedding' 
    AND deleted_at IS NULL
""")
embed_models = cur.fetchall()
for m in embed_models:
    print(f"  {m['name']} (id: {m['id']}) - is_default: {m['is_default']}")

cur.close()
conn.close()

print("\n--- Solution ---")
print("你已经有智谱 embedding-3 了！")
print("去 WeKnora 网页的：")
print("1. 模型管理 → 把 embedding-3 设为默认")
print("2. 知识库设置 → 确认 Embedding 模型选的是 embedding-3")
print("然后重新测试搜索！")

