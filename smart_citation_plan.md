# 智能引用添加方案

## 核心思路
不追求完美匹配，而是基于"相关性"添加引用

## 实现方案

### 方案A：段落级相关性匹配
```go
func addCitations(answer string, searchResults []*SearchResult) string {
    paragraphs := splitParagraphs(answer)
    
    for i, para := range paragraphs {
        // 计算段落与每个资料的相关性
        bestMatch := findBestMatch(para, searchResults)
        
        // 在段落末尾添加最相关资料的引用
        if bestMatch.Score > 0.6 {  // 阈值
            paragraphs[i] = para + fmt.Sprintf(" <kb doc=\"%s\" />", bestMatch.Title)
        }
    }
    
    return strings.Join(paragraphs, "\n\n")
}
```

### 方案B：强制引用所有来源
如果无法精确匹配，就在回答末尾列出所有参考来源：
```
[参考资料]
- 《当代占星研究》
- 《星座第一书》
```

### 方案C：混合方案（推荐）
1. 尝试段落级匹配，为相关性高的段落添加引用
2. 对于无法匹配的内容，在末尾列出所有来源
3. 标注"以上内容基于以下资料整理"

## 简化版实现
考虑到复杂性，可以先实现一个简化版：

```go
func addCitationsSimple(answer string, sources []KnowledgeInterpretSource) string {
    // 在回答末尾添加所有来源
    citation := "\n\n---\n**参考来源：**\n"
    for i, src := range sources {
        citation += fmt.Sprintf("%d. 《%s》\n", i+1, src.Title)
    }
    return answer + citation
}
```

## 优势
- 简单可靠，不会出错
- 用户知道答案基于哪些资料
- 即使AI没有内联引用，也有来源追溯

## 劣势
- 不是精确的内联引用
- 无法知道具体哪句话来自哪本书
