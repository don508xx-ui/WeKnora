package main

import (
	"context"
	"fmt"
	"os"
	"os/signal"
	"syscall"

	"github.com/Tencent/WeKnora/internal/config"
	"github.com/Tencent/WeKnora/internal/container"
	"github.com/Tencent/WeKnora/internal/logger"
	"github.com/Tencent/WeKnora/internal/router"
	"go.uber.org/dig"
)

func main() {
	ctx := context.Background()

	// Load configuration
	cfg, err := config.LoadConfig()
	if err != nil {
		fmt.Printf("Failed to load config: %v\n", err)
		os.Exit(1)
	}

	// Build dependency injection container
	diContainer := dig.New()
	container.BuildContainer(diContainer)

	// Initialize router and start server
	var r *router.Router
	err = diContainer.Invoke(func(router *router.Router) {
		r = router
	})
	if err != nil {
		fmt.Printf("Failed to get router: %v\n", err)
		os.Exit(1)
	}

	// Start server in a goroutine
	go func() {
		port := cfg.Server.Port
		if port == "" {
			port = "8080"
		}
		logger.Infof(ctx, "Starting server on port %s", port)
		if err := r.Run(":" + port); err != nil {
			logger.Errorf(ctx, "Failed to run server: %v", err)
			os.Exit(1)
		}
	}()

	// Wait for interrupt signal
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit

	logger.Infof(ctx, "Shutting down server...")
}
