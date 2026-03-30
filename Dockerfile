# 使用更小的 Alpine 基础镜像
FROM golang:1.24-alpine AS builder

WORKDIR /app

ARG GOPRIVATE_ARG
ARG GOPROXY_ARG
ARG GOSUMDB_ARG=off
ARG APK_MIRROR_ARG

ENV GOPRIVATE=${GOPRIVATE_ARG}
ENV GOPROXY=${GOPROXY_ARG}
ENV GOSUMDB=${GOSUMDB_ARG}

# 安装必要的构建依赖
RUN apk add --no-cache git build-base sqlite-dev

RUN go install -tags 'postgres' github.com/golang-migrate/migrate/v4/cmd/migrate@latest

# 先复制依赖文件，利用缓存
COPY go.mod go.sum ./
RUN --mount=type=cache,target=/go/pkg/mod go mod download

# 下载 DuckDB
COPY cmd/download cmd/download
RUN go run cmd/download/duckdb/duckdb.go

# 复制剩余文件
COPY . .

ARG VERSION_ARG
ARG COMMIT_ID_ARG
ARG BUILD_TIME_ARG
ARG GO_VERSION_ARG

ENV VERSION=${VERSION_ARG}
ENV COMMIT_ID=${COMMIT_ID_ARG}
ENV BUILD_TIME=${BUILD_TIME_ARG}
ENV GO_VERSION=${GO_VERSION_ARG}

# 构建应用
RUN --mount=type=cache,target=/go/pkg/mod make build-prod
RUN --mount=type=cache,target=/go/pkg/mod cp -r /go/pkg/mod/github.com/yanyiwu/ /app/yanyiwu/

# 使用更小的 Alpine 基础镜像作为最终阶段
FROM alpine:3.19

WORKDIR /app

# 安装必要的运行时依赖
RUN apk add --no-cache \
    ca-certificates tzdata curl bash \
    sqlite-libs \
    python3 py3-pip \
    nodejs npm \
    su-exec

# 创建用户
RUN adduser -D -s /bin/bash appuser

# 创建必要的目录
RUN mkdir -p /data/files && \
    chown -R appuser:appuser /app /data/files

# 从构建阶段复制文件
COPY --from=builder /go/bin/migrate /usr/local/bin/
COPY --from=builder /app/yanyiwu/ /go/pkg/mod/github.com/yanyiwu/
COPY --from=builder /app/config ./config
COPY --from=builder /app/scripts ./scripts
COPY --from=builder /app/migrations ./migrations
COPY --from=builder /app/dataset/samples ./dataset/samples
COPY --from=builder /app/skills/preloaded ./skills/preloaded
COPY --from=builder /app/skills/preloaded ./skills/_builtin
COPY --from=builder /root/.duckdb /home/appuser/.duckdb
COPY --from=builder /app/WeKnora .

# 复制入口点脚本
COPY --from=builder /app/scripts/docker-entrypoint.sh ./scripts/docker-entrypoint.sh

# 修改入口点脚本，使用 su-exec 替代 gosu
RUN sed -i 's/gosu/su-exec/g' ./scripts/docker-entrypoint.sh && \
    chmod +x ./scripts/*.sh

EXPOSE 8080

ENTRYPOINT ["./scripts/docker-entrypoint.sh"]
CMD ["./WeKnora"]