
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


def check_database(config, name):
    print(f"\n{'='*60}")
    print(f"检查 {name}")
    print(f"{'='*60}")

    try:
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()

        # 获取所有表
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        tables = cursor.fetchall()

        print(f"\n找到 {len(tables)} 个表:")
        for table in tables:
            print(f"  - {table[0]}")

        # 检查 schema_migrations 表（如果有）
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'schema_migrations'
            )
        """)
        has_migrations = cursor.fetchone()[0]

        if has_migrations:
            print(f"\nschema_migrations 表存在")
            cursor.execute("SELECT version, dirty FROM schema_migrations")
            result = cursor.fetchone()
            if result:
                print(f"当前迁移版本: {result[0]}, dirty: {result[1]}")

        conn.close()
        return [t[0] for t in tables]

    except Exception as e:
        print(f"连接失败: {e}")
        return []


def main():
    old_tables = check_database(OLD_DB_CONFIG, "旧数据库")
    new_tables = check_database(NEW_DB_CONFIG, "新数据库")

    print(f"\n{'='*60}")
    print("对比")
    print(f"{'='*60}")

    missing_in_new = set(old_tables) - set(new_tables)
    extra_in_new = set(new_tables) - set(old_tables)

    if missing_in_new:
        print(f"\n新数据库缺少的表: {sorted(missing_in_new)}")

    if extra_in_new:
        print(f"\n新数据库额外的表: {sorted(extra_in_new)}")

    if not missing_in_new and not extra_in_new:
        print("\n两个数据库表结构一致！")


if __name__ == "__main__":
    main()

