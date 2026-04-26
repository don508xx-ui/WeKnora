
import psycopg2

# 旧数据库
OLD_DB = "host=124.156.200.84 port=30815 user=root password=ln6RtXI590Sva2pNomAc7O1T4BPi38Ew dbname=zeabur sslmode=disable"

# 新数据库
NEW_DB = "host=124.156.200.84 port=32530 user=zeabur_user password=ZkO1xpqj4H95U7L6R3JSbKgF2WC8XI0u dbname=zeabur_db sslmode=disable"


def check_extensions(conn, name):
    print("Checking " + name + " extensions...")
    cur = conn.cursor()
    cur.execute("SELECT extname FROM pg_extension")
    exts = [row[0] for row in cur.fetchall()]
    print("  Installed: " + str(exts))
    cur.close()
    return exts


def main():
    print("Old DB:")
    old_conn = psycopg2.connect(OLD_DB)
    old_exts = check_extensions(old_conn, "old")
    old_conn.close()
    
    print("\nNew DB:")
    new_conn = psycopg2.connect(NEW_DB)
    new_exts = check_extensions(new_conn, "new")
    new_conn.close()


if __name__ == "__main__":
    main()

