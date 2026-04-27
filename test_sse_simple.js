const https = require('https');

const API_BASE_URL = 'wiki258.zeabur.app';
const API_KEY = 'sk-4xccX3jgVIo3Uc1Iu5GltBZg2JJ55gM8qwFzvJyCAo4ad-Zc';
const KNOWLEDGE_BASE_ID = '4b1c1c0a-64d4-4d3b-b605-0f984e66b7c8';

const postData = JSON.stringify({
  knowledge_base_ids: [KNOWLEDGE_BASE_ID],
  query: '金牛座特点',
  model_id: '',
  stream: true
});

const options = {
  hostname: API_BASE_URL,
  port: 443,
  path: '/api/v1/knowledge-interpret',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': API_KEY
  }
};

console.log('🚀 测试SSE流式输出');
console.log('='.repeat(60));

const req = https.request(options, (res) => {
  res.setEncoding('utf8');
  
  res.on('data', (chunk) => {
    console.log('📦 收到数据块:');
    console.log(chunk);
    console.log('---');
  });

  res.on('end', () => {
    console.log('✅ 流结束');
  });
});

req.on('error', (error) => {
  console.error('❌ 错误:', error);
});

req.write(postData);
req.end();
