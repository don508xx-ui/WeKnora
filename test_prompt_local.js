// 本地测试脚本 - 直接调用API验证prompt效果
const axios = require('axios');

// 模拟system prompt
const systemPrompt = `You are WeKnora, a professional intelligent information retrieval assistant. Answer based on the retrieved information below.

### Retrieved Information:
[1] Source: 当代占星研究
太阳星座代表一个人的核心自我、人生目标和意志力，是性格的骨架。

[2] Source: 星座第一书
月亮星座反映内在情绪、安全感和潜意识反应，是性格的血肉。

### Final Output Standards (STRICT):
*   **Sourced (Inline Citations):** EVERY factual claim must be cited using <kb doc="DOCUMENT_NAME" /> format.
    **Citation rules (ABSOLUTE):**
    - The citation tag must be placed ON THE SAME LINE as the last sentence of the paragraph it supports, with NO line break before it.
    - The DOCUMENT_NAME must match exactly with the "Source: XXX" labels in the Retrieved Information above.
    - Do NOT repeat the same citation after every sentence. One citation per paragraph per source is enough.
    - NEVER group all citations at the bottom of the answer. They must be distributed inline throughout the text.
    - CORRECT: 太阳星座代表核心自我。<kb doc="当代占星研究" />
    - WRONG (line break before tag):
      太阳星座代表核心自我。
      <kb doc="当代占星研究" />

### Task:
Answer the user's question based ONLY on the retrieved information above. Use zh-CN.`;

// 测试问题
const userQuery = "太阳星座和月亮星座分别代表什么？";

// 调用API
async function testPrompt() {
    try {
        const response = await axios.post('YOUR_API_ENDPOINT', {
            model: "glm-4",
            messages: [
                { role: "system", content: systemPrompt },
                { role: "user", content: userQuery }
            ],
            temperature: 0.7,
            stream: false
        }, {
            headers: {
                'Authorization': 'Bearer YOUR_API_KEY',
                'Content-Type': 'application/json'
            }
        });

        console.log("=== AI回答 ===");
        console.log(response.data.choices[0].message.content);
        
        // 检查是否包含引用
        const answer = response.data.choices[0].message.content;
        const hasCitation = answer.includes('<kb doc="');
        console.log("\n=== 验证结果 ===");
        console.log(`包含引用标签: ${hasCitation}`);
        
        if (hasCitation) {
            const citations = answer.match(/<kb doc="([^"]+)" \/>/g);
            console.log(`引用数量: ${citations.length}`);
            console.log(`引用内容: ${citations.join(', ')}`);
        }
        
    } catch (error) {
        console.error("测试失败:", error.message);
    }
}

testPrompt();
