package service

// 完全复刻WeKnora的Agent模式 - 直接调用AgentQA

import (
	"context"

	"github.com/Tencent/WeKnora/internal/event"
	"github.com/Tencent/WeKnora/internal/logger"
	"github.com/Tencent/WeKnora/internal/types"
)

// KnowledgeQA 直接复用AgentQA的实现，确保引用格式完全一致
func (s *sessionService) KnowledgeQA(
	ctx context.Context,
	req *types.QARequest,
	eventBus *event.EventBus,
) error {
	sessionID := req.Session.ID
	logger.Infof(ctx, "KnowledgeQA called for session: %s, query: %s", sessionID, req.Query)

	// 直接复用AgentQA的逻辑，但使用默认配置
	// 创建一个默认的CustomAgent配置来启用Agent模式
	if req.CustomAgent == nil {
		req.CustomAgent = &types.CustomAgent{
			ID:   "default-knowledge-qa",
			Name: "Default Knowledge QA",
			Config: types.CustomAgentConfig{
				AgentMode:        "smart-reasoning", // 启用Agent模式
				MaxIterations:    5,
				Temperature:      0.7,
				WebSearchEnabled: req.WebSearchEnabled,
				MultiTurnEnabled: false, // KnowledgeQA通常是单轮
				// 使用系统默认的模型配置
			},
		}
		logger.Infof(ctx, "Created default custom agent for KnowledgeQA")
	}

	// 确保Agent模式启用
	req.CustomAgent.Config.AgentMode = "smart-reasoning"

	// 直接调用AgentQA - 完全复用WeKnora的Agent实现
	logger.Infof(ctx, "Delegating KnowledgeQA to AgentQA for session: %s", sessionID)
	return s.AgentQA(ctx, req, eventBus)
}
