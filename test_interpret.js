const axios = require('axios');

const API_URL = 'https://wiki258.zeabur.app/api/v1/knowledge-interpret';

const test = async () => {
  try {
    const response = await axios.post(API_URL, {
      query: "你好，请介绍一下",
      knowledge_base_ids: ["你的知识库ID"],
    }, {
      headers: {
        'X-API-Key': '你的API Key',
        'Content-Type': 'application/json'
      }
    });

    console.log('✅ Success!');
    console.log('Answer:', response.data.answer);
    console.log('Model:', response.data.model);
    console.log('Sources:', response.data.sources);
  } catch (error) {
    console.error('❌ Error:', error.response?.data || error.message);
  }
};

test();
