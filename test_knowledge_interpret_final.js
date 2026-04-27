const https = require('https');
const fs = require('fs');

const API_BASE_URL = 'wiki258.zeabur.app';
const API_KEY = 'sk-4xccX3jgVIo3Uc1Iu5GltBZg2JJ55gM8qwFzvJyCAo4ad-Zc';
const KNOWLEDGE_BASE_ID = '4b1c1c0a-64d4-4d3b-b605-0f984e66b7c8';

function testKnowledgeInterpret(query) {
  return new Promise((resolve, reject) => {
    const postData = JSON.stringify({
      knowledge_base_ids: [KNOWLEDGE_BASE_ID],
      query: query,
      model_id: ''
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

    console.log('📤 发送请求...');
    console.log('🔍 查询:', query);
    console.log('📡 API路径:', options.path);
    console.log('');

    const req = https.request(options, (res) => {
      let data = '';

      res.on('data', (chunk) => {
        data += chunk;
      });

      res.on('end', () => {
        console.log('📥 收到响应，状态码:', res.statusCode);
        console.log('');
        
        try {
          const result = JSON.parse(data);
          resolve(result);
        } catch (e) {
          console.log('⚠️ 响应不是有效的JSON:', data);
          resolve({ raw: data });
        }
      });
    });

    req.on('error', (error) => {
      console.error('❌ 请求错误:', error);
      reject(error);
    });

    req.write(postData);
    req.end();
  });
}

async function runTests() {
  console.log('🧪 开始测试知识解读API');
  console.log('=' .repeat(60));
  console.log('');

  try {
    // 测试1: 查询金牛座特点
    console.log('🧪 测试1: 查询金牛座特点');
    const result1 = await testKnowledgeInterpret('金牛座特点');
    
    console.log('✅ 测试1结果:');
    console.log('  成功:', result1.success);
    console.log('  模型:', result1.model);
    console.log('  来源数量:', result1.sources?.length || 0);
    console.log('  答案长度:', result1.answer?.length || 0);
    console.log('');
    console.log('📝 答案内容:');
    console.log(result1.answer);
    console.log('');

    // 保存结果
    fs.writeFileSync('interpret_final_result.json', JSON.stringify(result1, null, 2), 'utf8');
    console.log('💾 结果已保存到 interpret_final_result.json');
    console.log('');

    console.log('=' .repeat(60));
    console.log('🎉 所有测试完成!');

  } catch (error) {
    console.error('❌ 测试失败:', error);
  }
}

runTests();
