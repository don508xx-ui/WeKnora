
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

# 新数据库配置
NEW_DB_CONFIG = {
    'host': '124.156.200.84',
    'port': '32530',
    'user': 'zeabur_user',
    'password': 'ZkO1xpqj4H95U7L6R3JSbKgF2WC8XI0u',
    'dbname': 'zeabur_db',
    'sslmode': 'disable'
}

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


def get_table_count(config, table_name):
    conn = psycopg2.connect(**config)
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    conn.close()
    return count


def main():
    print("对比两个数据库数据量...")
    print()

    for table in TABLES:
        try:
            old_count = get_table_count(OLD_DB_CONFIG, table)
            new_count = get_table_count(NEW_DB_CONFIG, table)
            print(table + ": " + str(old_count) + " (旧) | " + str(new_count) + " (新)")
        except Exception as e:
            print(table + ": ERROR - " + str(e))


if __name__ == "__main__":
    main()

