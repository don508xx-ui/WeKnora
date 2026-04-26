const https = require('https');
const fs = require('fs');

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
  console.log('Content-Type:', res.headers['content-type']);
  console.log('');

  let body = '';
  res.on('data', (chunk) => {
    body += chunk;
  });

  res.on('end', () => {
    // 保存到文件，用 UTF-8 编码
    fs.writeFileSync('response.json', body, 'utf8');
    console.log('响应已保存到 response.json');

    // 读取并显示
    const json = JSON.parse(body);
    if (json.data && json.data.length > 0) {
      const first = json.data[0];
      console.log('\n=== 中文内容 ===');
      console.log('文件名:', first.knowledge_filename);
      console.log('标题:', first.knowledge_title);
      console.log('');
      console.log('内容前200字:');
      console.log(first.matched_content?.substring(0, 200));
    }
  });
});

req.on('error', (e) => {
  console.error('请求错误:', e.message);
});

req.write(data);
req.end();
