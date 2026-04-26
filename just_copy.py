
import psycopg2
from psycopg2.extras import RealDictCursor
import json

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

# 按顺序复制的表
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
    'kb_shares',
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


def copy_table(table_name):
    print("=== " + table_name + " ===")
    
    # Read old data
    old_cur = OLD.cursor(cursor_factory=RealDictCursor)
    old_cur.execute("SELECT * FROM " + table_name)
    rows = old_cur.fetchall()
    old_cur.close()
    print("  Old rows: " + str(len(rows)))
    
    if not rows:
        print("  No data to copy")
        return 0
    
    # Truncate new table
    new_cur = NEW.cursor()
    try:
        new_cur.execute("TRUNCATE TABLE " + table_name + " CASCADE")
        NEW.commit()
    except Exception as e:
        print("  Truncate error (maybe table doesn't exist): " + str(e))
        NEW.rollback()
        # Try delete instead
        try:
            new_cur.execute("DELETE FROM " + table_name)
            NEW.commit()
        except Exception as e2:
            print("  Delete error too: " + str(e2))
            NEW.rollback()
            # Just continue and try insert anyway
            pass
    new_cur.close()
    
    # Insert into new
    new_cur = NEW.cursor()
    count = 0
    for row in rows:
        cols = list(row.keys())
        vals = []
        for v in row.values():
            if isinstance(v, dict):
                vals.append(psycopg2.extras.Json(v))
            else:
                vals.append(v)
        
        placeholders = ','.join(['%s'] * len(vals))
        sql = "INSERT INTO " + table_name + " (" + ','.join(cols) + ") VALUES (" + placeholders + ")"
        
        try:
            new_cur.execute(sql, vals)
            count += 1
        except Exception as e:
            print("  Insert error (row " + str(count+1) + "): " + str(e))
            NEW.rollback()
            # Try inserting without some fields?
            # For now, skip this row and continue
            print("  Skipping row")
            continue
    
    NEW.commit()
    new_cur.close()
    print("  Copied: " + str(count) + " rows")
    return count


def main():
    print("Starting copy...\n")
    
    total = 0
    for table in TABLES:
        try:
            total += copy_table(table)
        except Exception as e:
            print("  ERROR copying " + table + ": " + str(e))
            try:
                NEW.rollback()
            except:
                pass
        print("")
    
    OLD.close()
    NEW.close()
    print("Done! Total copied: " + str(total) + " rows")


if __name__ == "__main__":
    main()

