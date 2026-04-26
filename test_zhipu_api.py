
import requests
import json

print("=== Testing Zhipu API ===\n")

API_KEY = "be22125cefac4ed18e719e6cce2538ab.bKjo49kyKARv015U"
BASE_URL = "https://open.bigmodel.cn/api/paas/v4"

# 1. 先测试简单的 API 调用（比如 list models）
print("1. Testing API Key...")
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

try:
    # 测试模型列表
    response = requests.get(f"{BASE_URL}/models", headers=headers, timeout=10)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        print("   ✅ API Key 有效！")
        models_data = response.json()
        print(f"   Models found: {len(models_data.get('data', []))}")
    else:
        print(f"   ❌ API Key 无效！")
        print(f"   Response: {response.text}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 2. 测试 Embedding API
print("\n2. Testing Embedding API...")
embed_payload = {
    "model": "embedding-3",
    "input": "你好世界"
}

try:
    embed_response = requests.post(
        f"{BASE_URL}/embeddings",
        headers=headers,
        json=embed_payload,
        timeout=10
    )
    print(f"   Status: {embed_response.status_code}")
    
    if embed_response.status_code == 200:
        print("   ✅ Embedding API 正常！")
        embed_result = embed_response.json()
        print(f"   Embedding dimension: {len(embed_result['data'][0]['embedding'])}")
    else:
        print(f"   ❌ Embedding API 失败！")
        print(f"   Response: {embed_response.text}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n=== Test Done ===")

