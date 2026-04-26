
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


def main():
    print("修复新数据库迁移状态...")

    try:
        conn = psycopg2.connect(**NEW_DB_CONFIG)
        cursor = conn.cursor()

        # 检查当前状态
        cursor.execute("SELECT version, dirty FROM schema_migrations")
        version, dirty = cursor.fetchone()
        print(f"当前状态: version={version}, dirty={dirty}")

        if dirty:
            print("修复 dirty 状态...")
            # 强制设置为 version 1（不 dirty）
            cursor.execute("UPDATE schema_migrations SET dirty = false WHERE version = 2")
            conn.commit()
            print("已修复")

        # 检查
        cursor.execute("SELECT version, dirty FROM schema_migrations")
        version, dirty = cursor.fetchone()
        print(f"修复后状态: version={version}, dirty={dirty}")

        conn.close()
        print("\n✅ 状态修复完成！现在可以重启应用让它运行完整迁移到版本 31")

    except Exception as e:
        print(f"错误: {e}")


if __name__ == "__main__":
    main()

