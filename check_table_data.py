
import psycopg2

# 旧数据库配置
OLD_DB_CONFIG = {
    'host': '124.156.200.84',
    'port': '30815',
    'user': 'root',
    'password': 'ln6RtXI590Sva2pNomAc7O1T4BPi38Ew',
    'dbname': 'zeabur',
    'sslmode': 'disable'
}

# 需要检查的表
TABLES = [
    'tenants',
    'organizations',
    'users',
    'organization_members',
    'organization_join_requests',
    'models',
    'knowledge_bases',
    'knowledges',
    'knowledge_tags',
    'chunks',
    'embeddings',
    'lite_embeddings',
    'sessions',
    'messages',
    'custom_agents',
    'agent_shares',
    'tenant_disabled_shared_agents',
    'im_channels',
    'im_channel_sessions',
    'data_sources',
    'sync_logs',
    'mcp_services',
    'web_search_providers',
    'auth_tokens'
]


def main():
    print("检查旧数据库各表数据量...")

    try:
        conn = psycopg2.connect(**OLD_DB_CONFIG)
        cursor = conn.cursor()

        total_rows = 0
        for table in TABLES:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"{table}: {count} 条")
            total_rows += count

        print(f"\n总计: {total_rows} 条记录")
        conn.close()

    except Exception as e:
        print(f"错误: {e}")


if __name__ == "__main__":
    main()

