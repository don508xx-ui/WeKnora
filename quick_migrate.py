
import psycopg2
from psycopg2.extras import RealDictCursor
import json

# 旧数据库
OLD_DB = "host=124.156.200.84 port=30815 user=root password=ln6RtXI590Sva2pNomAc7O1T4BPi38Ew dbname=zeabur sslmode=disable"

# 新数据库
NEW_DB = "host=124.156.200.84 port=32530 user=zeabur_user password=ZkO1xpqj4H95U7L6R3JSbKgF2WC8XI0u dbname=zeabur_db sslmode=disable"


def get_old_schema_version(conn):
    cur = conn.cursor()
    cur.execute("SELECT version, dirty FROM schema_migrations")
    ver, dirty = cur.fetchone()
    cur.close()
    return ver, dirty


def set_new_schema_version(conn, version, dirty):
    cur = conn.cursor()
    cur.execute("UPDATE schema_migrations SET version = %s, dirty = %s", (version, dirty))
    conn.commit()
    cur.close()


def copy_table(old_conn, new_conn, table_name):
    print("Copying " + table_name + "...")
    
    old_cur = old_conn.cursor(cursor_factory=RealDictCursor)
    old_cur.execute("SELECT * FROM " + table_name)
    rows = old_cur.fetchall()
    old_cur.close()
    
    if not rows:
        print("  No data")
        return 0
    
    # Truncate new table
    new_cur = new_conn.cursor()
    new_cur.execute("TRUNCATE TABLE " + table_name + " CASCADE")
    new_conn.commit()
    new_cur.close()
    
    # Insert data
    new_cur = new_conn.cursor()
    
    for row in rows:
        cols = list(row.keys())
        vals = list(row.values())
        
        processed_vals = []
        for v in vals:
            if isinstance(v, dict):
                processed_vals.append(psycopg2.extras.Json(v))
            else:
                processed_vals.append(v)
        
        placeholders = ','.join(['%s'] * len(processed_vals))
        sql = "INSERT INTO " + table_name + " (" + ','.join(cols) + ") VALUES (" + placeholders + ")"
        new_cur.execute(sql, processed_vals)
    
    new_conn.commit()
    new_cur.close()
    print("  Copied " + str(len(rows)) + " rows")
    return len(rows)


def main():
    print("Connecting to old DB...")
    old_conn = psycopg2.connect(OLD_DB)
    
    print("Connecting to new DB...")
    new_conn = psycopg2.connect(NEW_DB)
    
    # Get old version
    old_ver, old_dirty = get_old_schema_version(old_conn)
    print("Old DB schema version: " + str(old_ver) + ", dirty: " + str(old_dirty))
    
    # Set new version to match
    print("Setting new DB schema version to " + str(old_ver) + "...")
    set_new_schema_version(new_conn, old_ver, old_dirty)
    
    # Copy tables
    tables = [
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
    
    total = 0
    for table in tables:
        try:
            total += copy_table(old_conn, new_conn, table)
        except Exception as e:
            print("  ERROR copying " + table + ": " + str(e))
            # Continue with next table
            try:
                new_conn.rollback()
            except:
                pass
    
    old_conn.close()
    new_conn.close()
    print("\nTotal copied: " + str(total) + " rows")
    print("Done! Now you can switch the app to use the new DB.")


if __name__ == "__main__":
    main()

