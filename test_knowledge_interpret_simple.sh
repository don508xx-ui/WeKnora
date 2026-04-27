#!/bin/bash
# 简单测试脚本，等 Zeabur 部署完成后使用

# 配置
API_URL="https://wiki258.zeabur.app/api/v1/knowledge-interpret"

# 测试用的数据
# 注意：需要替换为真实的知识库ID和测试问题
TEST_DATA='{
  "query": "这是一个测试问题",
  "knowledge_base_ids": ["YOUR_KB_ID"],
  "model_id": ""
}'

echo "测试 Knowledge Interpret 接口..."
echo "URL: $API_URL"
echo ""

# 发送 POST 请求
curl -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -d "$TEST_DATA" \
  -w "\n\nHTTP 状态码: %{http_code}\n"
