
import psycopg2
from psycopg2.extras import RealDictCursor

# 旧数据库
OLD_DB = "host=124.156.200.84 port=30815 user=root password=ln6RtXI590Sva2pNomAc7O1T4BPi38Ew dbname=zeabur sslmode=disable"

# 新数据库
NEW_DB = "host=124.156.200.84 port=32530 user=zeabur_user password=ZkO1xpqj4H95U7L6R3JSbKgF2WC8XI0u dbname=zeabur_db sslmode=disable"

# 按顺序迁移的表
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


def migrate_table(table_name, old_conn, new_conn):
    print("Migrating " + table_name + "...")
    
    # Read from old
    old_cur = old_conn.cursor(cursor_factory=RealDictCursor)
    old_cur.execute("SELECT * FROM " + table_name)
    rows = old_cur.fetchall()
    old_cur.close()
    
    if not rows:
        print("  No data")
        return 0
    
    # Write to new
    new_cur = new_conn.cursor()
    
    for row in rows:
        cols = list(row.keys())
        vals = list(row.values())
        
        # Convert dicts to JSON strings
        processed_vals = []
        for v in vals:
            if isinstance(v, dict):
                import json
                processed_vals.append(json.dumps(v))
            else:
                processed_vals.append(v)
        
        placeholders = ','.join(['%s'] * len(processed_vals))
        sql = "INSERT INTO " + table_name + " (" + ','.join(cols) + ") VALUES (" + placeholders + ")"
        new_cur.execute(sql, processed_vals)
    
    new_conn.commit()
    new_cur.close()
    print("  Done, " + str(len(rows)) + " rows")
    return len(rows)


def main():
    print("Connecting to old DB...")
    old_conn = psycopg2.connect(OLD_DB)
    print("Connecting to new DB...")
    new_conn = psycopg2.connect(NEW_DB)
    
    total = 0
    for table in TABLES:
        try:
            total += migrate_table(table, old_conn, new_conn)
        except Exception as e:
            print("  ERROR: " + str(e))
            # Try to continue
            new_conn.rollback()
    
    old_conn.close()
    new_conn.close()
    print("\nTotal migrated: " + str(total) + " rows")


if __name__ == "__main__":
    main()

