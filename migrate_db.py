
import psycopg2
from psycopg2.extras import RealDictCursor
import json
from datetime import datetime

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

# 需要迁移的表（按外键依赖顺序排列）
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


def copy_table_data(old_conn, new_conn, table_name):
    print("正在迁移表: " + table_name)

    try:
        old_cursor = old_conn.cursor(cursor_factory=RealDictCursor)
        new_cursor = new_conn.cursor()

        old_cursor.execute("SELECT * FROM " + table_name)
        rows = old_cursor.fetchall()

        if not rows:
            print("表 " + table_name + " 没有数据")
            return 0

        print("找到 " + str(len(rows)) + " 条记录")

        for row in rows:
            columns = list(row.keys())
            values = list(row.values())

            # 转换 dict 为 JSON 字符串
            processed_values = []
            for val in values:
                if isinstance(val, dict):
                    processed_values.append(psycopg2.extras.Json(val))
                else:
                    processed_values.append(val)

            placeholders = ','.join(['%s'] * len(processed_values))
            columns_str = ','.join(columns)

            sql = "INSERT INTO " + table_name + " (" + columns_str + ") VALUES (" + placeholders + ")"

            try:
                new_cursor.execute(sql, processed_values)
            except Exception as e:
                print("插入记录时出错: " + str(e))
                print("SQL: " + sql)
                raise

        new_conn.commit()
        print("表 " + table_name + " 迁移完成，共 " + str(len(rows)) + " 条记录")
        return len(rows)

    except Exception as e:
        print("迁移表 " + table_name + " 时出错: " + str(e))
        new_conn.rollback()
        raise
    finally:
        old_cursor.close()
        new_cursor.close()


def main():
    print("开始数据库迁移...")

    try:
        # 连接旧数据库
        print("连接旧数据库...")
        old_conn = psycopg2.connect(**OLD_DB_CONFIG)
        print("旧数据库连接成功")

        # 连接新数据库
        print("连接新数据库...")
        new_conn = psycopg2.connect(**NEW_DB_CONFIG)
        print("新数据库连接成功")

        total_rows = 0
        for table in TABLES:
            rows = copy_table_data(old_conn, new_conn, table)
            total_rows += rows

        print("\n迁移完成！共迁移 " + str(total_rows) + " 条记录")

    except Exception as e:
        print("迁移失败: " + str(e))
    finally:
        if 'old_conn' in locals():
            old_conn.close()
        if 'new_conn' in locals():
            new_conn.close()


if __name__ == "__main__":
    main()

