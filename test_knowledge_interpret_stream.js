const https = require('https');

const API_BASE_URL = 'wiki258.zeabur.app';
const API_KEY = 'sk-4xccX3jgVIo3Uc1Iu5GltBZg2JJ55gM8qwFzvJyCAo4ad-Zc';
const KNOWLEDGE_BASE_ID = '4b1c1c0a-64d4-4d3b-b605-0f984e66b7c8';

function testStreamingKnowledgeInterpret(query) {
  return new Promise((resolve, reject) => {
    const postData = JSON.stringify({
      knowledge_base_ids: [KNOWLEDGE_BASE_ID],
      query: query,
      model_id: '',
      stream: true  // Enable streaming
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

    console.log('🚀 开始流式知识解读测试');
    console.log('🔍 查询:', query);
    console.log('📡 API路径:', options.path);
    console.log('='.repeat(60));
    console.log('');

    let fullThinking = '';
    let fullAnswer = '';
    let sources = null;
    let model = null;

    const req = https.request(options, (res) => {
      res.setEncoding('utf8');
      let buffer = '';

      res.on('data', (chunk) => {
        buffer += chunk;
        
        while (true) {
          const doubleNewlineIndex = buffer.indexOf('\n\n');
          if (doubleNewlineIndex === -1) {
            break;
          }

          const eventStr = buffer.substring(0, doubleNewlineIndex);
          buffer = buffer.substring(doubleNewlineIndex + 2);
          processEvent(eventStr);
        }
      });

      res.on('end', () => {
        if (buffer.trim()) {
          processEvent(buffer.trim());
        }

        console.log('');
        console.log('='.repeat(60));
        console.log('📊 流式完成总结');
        console.log('   模型:', model);
        console.log('   来源数量:', sources?.length || 0);
        console.log('   思考长度:', fullThinking.length);
        console.log('   答案长度:', fullAnswer.length);
        resolve({
          thinking: fullThinking,
          answer: fullAnswer,
          sources: sources,
          model: model
        });
      });
    });

    function processEvent(eventStr) {
      if (!eventStr.startsWith('event: message')) {
        return;
      }

      let dataStart = eventStr.indexOf('data: ');
      if (dataStart === -1) {
        return;
      }
      
      const jsonStr = eventStr.substring(dataStart + 'data: '.length).trim();
      
      try {
        const response = JSON.parse(jsonStr);
        
        const responseType = response.response_type;
        const content = response.content || '';
        const done = response.done;

        if (responseType === 'sources') {
          const sourceData = JSON.parse(content);
          sources = sourceData.sources;
          model = sourceData.model;
          console.log('📚 来源信息:');
          console.log('   模型:', model);
          console.log('   来源:', JSON.stringify(sources, null, 2));
        } else if (responseType === 'thinking') {
          // Clean <think> tags if present
          let cleanContent = content;
          if (cleanContent.includes('<think>')) {
            const startIdx = cleanContent.indexOf('<think>') + '<think>'.length;
            const endIdx = cleanContent.indexOf('</think>');
            if (endIdx !== -1) {
              cleanContent = cleanContent.substring(startIdx, endIdx);
            } else {
              cleanContent = cleanContent.substring(startIdx);
            }
          }
          fullThinking += cleanContent;
          
          if (cleanContent.trim()) {
            process.stdout.write('🤔 ' + cleanContent);
          }
          if (done) {
            process.stdout.write('\n');
          }
        } else if (responseType === 'answer') {
          // Remove thinking tags if present
          let cleanContent = content.replace(/<think>.*?<\/think>/gs, '');
          fullAnswer += cleanContent;
          
          if (cleanContent.trim()) {
            process.stdout.write('💬 ' + cleanContent);
          }
          if (done) {
            process.stdout.write('\n');
          }
        } else if (responseType === 'error') {
          console.error('❌ 错误:', content);
        }
      } catch (e) {
        // Not valid JSON, might be partial data
      }
    }

    req.on('error', (error) => {
      console.error('❌ 请求错误:', error);
      reject(error);
    });

    req.write(postData);
    req.end();
  });
}

async function runTest() {
  try {
    const result = await testStreamingKnowledgeInterpret('金牛座特点');
    console.log('');
    console.log('🎉 测试完成！');
    console.log('');
    console.log('📝 完整思考内容:');
    console.log(result.thinking);
    console.log('');
    console.log('📝 完整答案内容:');
    console.log(result.answer);
  } catch (error) {
    console.error('❌ 测试失败:', error);
  }
}

runTest();
