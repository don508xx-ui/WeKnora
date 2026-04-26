
import psycopg2
from psycopg2.extras import RealDictCursor
import json

print("Connecting...")

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

# 按顺序迁移
tables = [
    'tenants',
    'organizations',
    'users',
    'organization_members',
    'organization_join_requests',
    'knowledge_bases',
    'knowledges',
    'knowledge_tags',
    'chunks',
    'embeddings',
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

total = 0

for table in tables:
    print("\n=== " + table + " ===")
    
    # 读旧数据
    old_cur = old_conn.cursor(cursor_factory=RealDictCursor)
    try:
        old_cur.execute("SELECT * FROM " + table)
        rows = old_cur.fetchall()
    except Exception as e:
        print("  读错误: " + str(e))
        old_cur.close()
        continue
    old_cur.close()
    
    print("  旧数据: " + str(len(rows)) + " 行")
    
    if len(rows) == 0:
        continue
    
    # 清空新表
    new_cur = new_conn.cursor()
    try:
        new_cur.execute("TRUNCATE TABLE " + table + " CASCADE")
        new_conn.commit()
    except Exception as e:
        print("  清空错误: " + str(e))
        new_conn.rollback()
        try:
            new_cur.execute("DELETE FROM " + table)
            new_conn.commit()
        except:
            new_conn.rollback()
    new_cur.close()
    
    # 插入新数据
    new_cur = new_conn.cursor()
    count = 0
    for row in rows:
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
            print("  插入错误 (行 " + str(count+1) + "): " + str(e))
            new_conn.rollback()
            # 继续下一行
            continue
    
    new_conn.commit()
    new_cur.close()
    
    print("  已复制: " + str(count) + " 行")
    total += count

old_conn.close()
new_conn.close()

print("\n=== 完成 ===")
print("总共复制: " + str(total) + " 行")
print("现在可以切换应用使用新数据库了！")

