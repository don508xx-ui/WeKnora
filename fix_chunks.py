
import psycopg2
from psycopg2.extras import RealDictCursor
import json

print("=== Fixing missing data ===\n")

# 旧数据库
old_conn = psycopg2.connect(
    host="124.156.200.84",
    port="30815",
    user="root",
    password="ln6RtXI590Sva2pNomAc7O1T4BPi38Ew",
    dbname="zeabur",
    sslmode="disable"
)

# 新数据库
new_conn = psycopg2.connect(
    host="124.156.200.84",
    port="32530",
    user="zeabur_user",
    password="ZkO1xpqj4H95U7L6R3JSbKgF2WC8XI0u",
    dbname="zeabur_db",
    sslmode="disable"
)

# 重要的表
tables = [
    'tenants',
    'users',
    'knowledge_bases',
    'knowledges',
    'chunks',
    'sessions',
    'messages',
    'custom_agents',
    'auth_tokens'
]

total = 0

for table in tables:
    print("\n--- " + table + " ---")
    
    # 读旧数据
    old_cur = old_conn.cursor(cursor_factory=RealDictCursor)
    old_cur.execute("SELECT * FROM " + table)
    old_rows = old_cur.fetchall()
    old_cur.close()
    print("  旧数据库: " + str(len(old_rows)) + " 行")
    
    if len(old_rows) == 0:
        continue
    
    # 查新数据库有多少
    new_cur = new_conn.cursor()
    new_cur.execute("SELECT COUNT(*) FROM " + table)
    new_cnt = new_cur.fetchone()[0]
    new_cur.close()
    print("  新数据库: " + str(new_cnt) + " 行")
    
    # 如果新数据库数据少，就清空重新复制
    if new_cnt < len(old_rows):
        print("  数据不完整，重新复制...")
        
        # 清空新表
        new_cur = new_conn.cursor()
        try:
            new_cur.execute("TRUNCATE TABLE " + table + " CASCADE")
            new_conn.commit()
        except:
            new_conn.rollback()
            new_cur.execute("DELETE FROM " + table)
            new_conn.commit()
        new_cur.close()
        
        # 复制
        new_cur = new_conn.cursor()
        count = 0
        for row in old_rows:
            cols = list(row.keys())
            vals = []
            for v in row.values():
                if isinstance(v, dict):
                    vals.append(json.dumps(v))
                else:
                    vals.append(v)
            
            placeholders = ','.join(['%s'] * len(vals))
            sql = "INSERT INTO " + table + " (" + ','.join(cols) + ") VALUES (" + placeholders + ")"
            try:
                new_cur.execute(sql, vals)
                count += 1
            except Exception as e:
                print("  插入错误: " + str(e))
                new_conn.rollback()
                continue
        
        new_conn.commit()
        new_cur.close()
        print("  已复制: " + str(count) + " 行")
        total += count
    else:
        print("  数据完整，跳过")

old_conn.close()
new_conn.close()

print("\n=== 完成 ===")
print("总共复制: " + str(total) + " 行")
print("现在刷新应用看看分块数据回来没有！")

