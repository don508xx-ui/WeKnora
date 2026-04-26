
import psycopg2
import json
import requests

print("=== Testing & Updating Model ===\n")

API_KEY = "be22125cefac4ed18e719e6cce2538ab.bKjo49kyKARv015U"

# 1. 测试 embedding API
print("1. Testing Embedding API...")
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}
embed_payload = {"model": "embedding-3", "input": "test"}
try:
    res = requests.post(
        "https://open.bigmodel.cn/api/paas/v4/embeddings",
        headers=headers,
        json=embed_payload,
        timeout=10
    )
    print(f"   Status: {res.status_code}")
    if res.status_code == 200:
        print("   Embedding API OK!")
except Exception as e:
    print(f"   Error: {e}")

# 2. 更新数据库里的模型
print("\n2. Updating model in DB...")

conn = psycopg2.connect(
    host="124.156.200.84",
    port="32530",
    user="zeabur_user",
    password="ZkO1xpqj4H95U7L6R3JSbKgF2WC8XI0u",
    dbname="zeabur_db",
    sslmode="disable"
)

cur = conn.cursor()

# 获取 embedding-3 的 id
cur.execute("SELECT id, parameters FROM models WHERE name = 'embedding-3' AND deleted_at IS NULL")
model = cur.fetchone()

if model:
    model_id = model[0]
    params = model[1]
    
    print(f"   Found model: {model_id}")
    print(f"   Updating API key...")
    
    # 更新参数 - 注意：WeKnora 用的是加密的，我们这里直接更新数据库，等下应用会重新保存一下
    # 实际上，更简单的方法是：你去 WeKnora 网页重新保存这个模型！
    
    print("\n--- Recommendation:")
    print("   Go to WeKnora Web -> Model Management -> Edit embedding-3 -> Re-save it!")
    print("   OR: Re-save with your new API key!")
else:
    print("   Model not found!")

cur.close()
conn.close()

print("\n=== Done ===")

