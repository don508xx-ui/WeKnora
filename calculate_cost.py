
import psycopg2

print("=== 知识库成本评估 ===\n")

conn = psycopg2.connect(
    host="124.156.200.84",
    port="32530",
    user="zeabur_user",
    password="ZkO1xpqj4H95U7L6R3JSbKgF2WC8XI0u",
    dbname="zeabur_db",
    sslmode="disable"
)

cur = conn.cursor()

# 1. 统计 chunks 和 embeddings
cur.execute("SELECT COUNT(*) FROM chunks WHERE deleted_at IS NULL")
chunks_count = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM embeddings")
embeddings_count = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM knowledges WHERE deleted_at IS NULL AND parse_status = 'completed'")
docs_count = cur.fetchone()[0]

print(f"当前数据量:")
print(f"  文档数: {docs_count}")
print(f"  分块数: {chunks_count}")
print(f"  向量化数: {embeddings_count}")

cur.close()
conn.close()

print("\n--- 成本估算 ---")
print("智谱 embedding-3 价格 (参考): 约 0.005元 / 1M tokens (输入)")
print("假设 1 个 chunk = 512 tokens\n")

# 计算初始构建成本
initial_tokens = chunks_count * 512
initial_cost = (initial_tokens / 1000000) * 0.005
print(f"  初始构建（{chunks_count} 个 chunk）:")
print(f"    Tokens: {initial_tokens:,}")
print(f"    成本: 约 {initial_cost:.4f} 元\n")

# 计算搜索成本（假设每天 100 次搜索）
search_queries_per_day = 100
search_tokens_per_query = 20  # 查询文本平均 20 tokens
daily_search_tokens = search_queries_per_day * search_tokens_per_query
daily_search_cost = (daily_search_tokens / 1000000) * 0.005
monthly_search_cost = daily_search_cost * 30
print(f"  搜索（假设每天 {search_queries_per_day} 次搜索）:")
print(f"    每天 Tokens: {daily_search_tokens:,}")
print(f"    每天成本: 约 {daily_search_cost:.6f} 元")
print(f"    每月成本: 约 {monthly_search_cost:.4f} 元\n")

print("--- 总结 ---")
print("✅ Embedding 成本非常低！")
print("   - 初始构建：几乎免费（不到 1 分钱）")
print("   - 搜索：每月也只要几分钱到几毛钱")
print("   - 主要成本其实在 LLM 问答上（不是 Embedding）")

