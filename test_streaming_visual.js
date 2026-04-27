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

console.log('🚀 测试流式输出视觉效果');
console.log('💡 这个测试会模拟打字机效果，逐字显示');
console.log('='.repeat(60));
console.log('');

let answer = '';
let chunkCount = 0;
let startTime = Date.now();

const req = https.request(options, (res) => {
  res.setEncoding('utf8');
  let buffer = '';
  
  res.on('data', (chunk) => {
    buffer += chunk;
    
    while (true) {
      const eventEnd = buffer.indexOf('\n\n');
      if (eventEnd === -1) break;
      
      const event = buffer.substring(0, eventEnd);
      buffer = buffer.substring(eventEnd + 2);
      
      if (event.startsWith('event:message')) {
        const dataMatch = event.match(/data:(.+)/);
        if (dataMatch) {
          try {
            const data = JSON.parse(dataMatch[1].trim());
            if (data.response_type === 'answer' && data.content) {
              chunkCount++;
              answer += data.content;
              // 清屏并重新打印
              process.stdout.write('\r' + ' '.repeat(80) + '\r');
              process.stdout.write('📝 ' + answer.substring(Math.max(0, answer.length - 70)));
            }
          } catch (e) {}
        }
      }
    }
  });

  res.on('end', () => {
    const duration = Date.now() - startTime;
    console.log('\n\n' + '='.repeat(60));
    console.log('✅ 流式完成！');
    console.log('   总耗时:', duration, 'ms');
    console.log('   数据块数:', chunkCount);
    console.log('   总字数:', answer.length);
    console.log('   平均速度:', (chunkCount / (duration / 1000)).toFixed(2), 'chunks/s');
    console.log('\n📝 完整答案:');
    console.log(answer);
  });
});

req.on('error', (error) => {
  console.error('❌ 错误:', error);
});

req.write(postData);
req.end();
