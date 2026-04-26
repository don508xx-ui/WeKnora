
import psycopg2
from psycopg2.extras import RealDictCursor

# 旧数据库
OLD = psycopg2.connect(
    host="124.156.200.84",
    port="30815",
    user="root",
    password="ln6RtXI590Sva2pNomAc7O1T4BPi38Ew",
    dbname="zeabur",
    sslmode="disable"
)

# 新数据库
NEW = psycopg2.connect(
    host="124.156.200.84",
    port="32530",
    user="zeabur_user",
    password="ZkO1xpqj4H95U7L6R3JSbKgF2WC8XI0u",
    dbname="zeabur_db",
    sslmode="disable"
)

# 核心表
TABLES = [
    'tenants',
    'users',
    'models',
    'knowledge_bases',
    'knowledges',
    'chunks',
    'sessions',
    'messages',
    'custom_agents'
]


def copy_table(table_name):
    print(table_name + "...")
    
    # 读旧数据
    old_cur = OLD.cursor(cursor_factory=RealDictCursor)
    old_cur.execute("SELECT * FROM " + table_name)
    rows = old_cur.fetchall()
    old_cur.close()
    print("  旧数据: " + str(len(rows)) + " 行")
    
    if not rows:
        return 0
    
    # 清空新表
    new_cur = NEW.cursor()
    try:
        new_cur.execute("TRUNCATE TABLE " + table_name + " CASCADE")
        NEW.commit()
    except:
        NEW.rollback()
        new_cur.execute("DELETE FROM " + table_name)
        NEW.commit()
    new_cur.close()
    
    # 插入新数据
    new_cur = NEW.cursor()
    count = 0
    for row in rows:
        cols = list(row.keys())
        vals = []
        for v in row.values():
            if isinstance(v, dict):
                import json
                vals.append(json.dumps(v))
            else:
                vals.append(v)
        
        placeholders = ','.join(['%s'] * len(vals))
        sql = "INSERT INTO " + table_name + " (" + ','.join(cols) + ") VALUES (" + placeholders + ")"
        
        try:
            new_cur.execute(sql, vals)
            count += 1
        except Exception as e:
            print("  插入错误: " + str(e))
            NEW.rollback()
            continue
    
    NEW.commit()
    new_cur.close()
    print("  已复制: " + str(count) + " 行")
    return count


def main():
    print("开始复制核心表...\n")
    
    total = 0
    for table in TABLES:
        try:
            total += copy_table(table)
        except Exception as e:
            print("  错误: " + str(e))
            try:
                NEW.rollback()
            except:
                pass
        print("")
    
    OLD.close()
    NEW.close()
    print("完成！总共复制: " + str(total) + " 行")


if __name__ == "__main__":
    main()

