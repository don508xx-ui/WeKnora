
import requests
import json

API_KEY = "be22125cefac4ed18e719e6cce2538ab.bKjo49kyKARv015U"
BASE_URL = "https://open.bigmodel.cn/api/paas/v4"

print("1. Testing List Models...")
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}
try:
    res = requests.get(f"{BASE_URL}/models", headers=headers, timeout=10)
    print(f"   Status: {res.status_code}")
    if res.status_code == 200:
        print("   API Key OK!")
except Exception as e:
    print(f"   Error: {e}")

print("\n2. Testing Embedding...")
try:
    embed_res = requests.post(
        f"{BASE_URL}/embeddings",
        headers=headers,
        json={"model": "embedding-3", "input": "test"},
        timeout=10
    )
    print(f"   Embedding Status: {embed_res.status_code}")
    if embed_res.status_code == 200:
        print("   Embedding OK!")
        data = embed_res.json()
        print(f"   Dimension: {len(data['data'][0]['embedding'])}")
    else:
        print(f"   Response: {embed_res.text}")
except Exception as e:
    print(f"   Error: {e}")

print("\n3. Testing Chat (glm-4.7-flash)...")
try:
    chat_res = requests.post(
        f"{BASE_URL}/chat/completions",
        headers=headers,
        json={
            "model": "glm-4.7-flash",
            "messages": [{"role": "user", "content": "你好"}],
            "max_tokens": 50
        },
        timeout=15
    )
    print(f"   Chat Status: {chat_res.status_code}")
    if chat_res.status_code == 200:
        print("   Chat OK!")
        chat_data = chat_res.json()
        print(f"   Response: {chat_data['choices'][0]['message']['content']}")
    else:
        print(f"   Response: {chat_res.text}")
except Exception as e:
    print(f"   Error: {e}")

print("\nDone!")
