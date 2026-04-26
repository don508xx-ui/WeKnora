
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
    print("检查新数据库有哪些表...")

    try:
        conn = psycopg2.connect(**NEW_DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)

        tables = [row[0] for row in cursor.fetchall()]

        print("新数据库表:")
        for table in tables:
            print("  - " + table)

        conn.close()

    except Exception as e:
        print("错误: " + str(e))


if __name__ == "__main__":
    main()

