
import psycopg2

# 新数据库配置
NEW_DB_CONFIG = {
    'host': '124.156.200.84',
    'port': '32530',
    'user': 'zeabur_user',
    'password': 'ZkO1xpqj4H95U7L6R3JSbKgF2WC8XI0u',
    'dbname': 'zeabur_db',
    'sslmode': 'disable'
}

# 要清空的表（按反顺序）
TABLES = [
    'auth_tokens',
    'web_search_providers',
    'mcp_services',
    'sync_logs',
    'data_sources',
    'im_channel_sessions',
    'im_channels',
    'tenant_disabled_shared_agents',
    'agent_shares',
    'custom_agents',
    'messages',
    'sessions',
    'lite_embeddings',
    'embeddings',
    'chunks',
    'knowledge_tags',
    'knowledges',
    'knowledge_bases',
    'models',
    'organization_join_requests',
    'organization_members',
    'users',
    'organizations',
    'tenants'
]


def main():
    print("清空新数据库数据...")

    try:
        conn = psycopg2.connect(**NEW_DB_CONFIG)
        cursor = conn.cursor()

        for table in TABLES:
            try:
                cursor.execute("DELETE FROM " + table)
                print("已清空表: " + table)
            except Exception as e:
                print("清空表 " + table + " 时出错: " + str(e))

        conn.commit()
        conn.close()
        print("\n数据已清空！现在可以运行迁移脚本了")

    except Exception as e:
        print("错误: " + str(e))


if __name__ == "__main__":
    main()

