
import psycopg2
from psycopg2.extras import RealDictCursor
import json

print("=== Checking Models Configuration ===\n")

conn = psycopg2.connect(
    host="124.156.200.84",
    port="32530",
    user="zeabur_user",
    password="ZkO1xpqj4H95U7L6R3JSbKgF2WC8XI0u",
    dbname="zeabur_db",
    sslmode="disable"
)

cur = conn.cursor(cursor_factory=RealDictCursor)
cur.execute("SELECT id, name, provider, model_id FROM models WHERE deleted_at IS NULL")
models = cur.fetchall()

print("Available Models (" + str(len(models)) + "):")
for m in models:
    print("  - " + str(m['name']) + " (" + str(m['provider']) + " / " + str(m['model_id']) + ")")

cur.close()
conn.close()

print("\n--- Problem & Solutions ---")
print("Problem: Baidu API 429 = 额度用完了！")
print("\nSolutions:")
print("1. 去百度控制台充值额度")
print("2. 改用其他 Embedding API（比如：智谱 embedding-3）")
print("3. 在 WeKnora 模型配置里切换 Embedding 模型")

