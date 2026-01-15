
import sqlite3

def check_schema():
    conn = sqlite3.connect('backend/todo.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    for table_name in tables:
        name = table_name[0]
        print(f"\nTable: {name}")
        cursor.execute(f"PRAGMA table_info({name})")
        columns = cursor.fetchall()
        for col in columns:
            print(col)
        
        cursor.execute(f"SELECT * FROM {name} LIMIT 5")
        rows = cursor.fetchall()
        print(f"Sample data from {name}:")
        for row in rows:
            print(list(row))
    
    conn.close()

if __name__ == "__main__":
    check_schema()
