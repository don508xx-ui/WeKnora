const https = require('https');

const options = {
  hostname: 'wiki258.zeabur.app',
  path: '/api/v1/knowledge-search',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': 'sk-4xccX3jgVIo3Uc1Iu5GltBZg2JJ55gM8qwFzvJyCAo4ad-Zc',
    'Accept': 'application/json'
  }
};

const data = JSON.stringify({
  query: "测试中文编码",
  knowledge_base_ids: ["4b1c1c0a-64d4-4d3b-b605-0f984e66b7c8"]
});

const req = https.request(options, (res) => {
  console.log('状态码:', res.statusCode);
  console.log('所有响应头:', JSON.stringify(res.headers, null, 2));
  console.log('');

  // 检查 Content-Type 是否包含 charset=utf-8
  const contentType = res.headers['content-type'];
  console.log('Content-Type:', contentType);
  if (contentType && contentType.includes('utf-8')) {
    console.log('✅ 服务端已设置 UTF-8 编码');
  } else {
    console.log('❌ 服务端未设置 UTF-8 编码');
  }
  console.log('');

  let body = '';
  res.on('data', (chunk) => {
    body += chunk;
  });

  res.on('end', () => {
    // 检查原始字节
    const buffer = Buffer.from(body);
    console.log('响应体字节长度:', buffer.length);
    console.log('响应体前100字节 (十六进制):', buffer.slice(0, 100).toString('hex'));
    console.log('');

    try {
      const json = JSON.parse(body);
      console.log('解析后的数据:');
      console.log('success:', json.success);

      // 检查是否有中文内容
      if (json.data && json.data.length > 0) {
        console.log('\n--- 中文内容检查 ---');
        const firstResult = json.data[0];
        console.log('knowledge_title:', firstResult.knowledge_title);
      }
    } catch (e) {
      console.log('解析错误:', e.message);
      console.log('原始响应前200字符:', body.substring(0, 200));
    }
  });
});

req.on('error', (e) => {
  console.error('请求错误:', e.message);
});

req.write(data);
req.end();
