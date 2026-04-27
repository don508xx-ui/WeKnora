@echo off
REM 简单测试脚本，等 Zeabur 部署完成后使用

REM 配置
set API_URL=https://wiki258.zeabur.app/api/v1/knowledge-interpret

echo 测试 Knowledge Interpret 接口...
echo URL: %API_URL%
echo.

REM 注意：需要替换为真实的知识库ID和测试问题
curl -X POST "%API_URL%" -H "Content-Type: application/json" -d "{\"query\":\"这是一个测试问题\",\"knowledge_base_ids\":[\"YOUR_KB_ID\"]}"

echo.
echo.
echo 请替换 YOUR_KB_ID 为真实的知识库ID！
