# scripts/setup_db.py
import os
from lib.db.connection import get_connection

def run_schema():
    # Compute absolute path to schema.sql (always from project root)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    schema_path = os.path.join(project_root, "lib", "db", "schema.sql")

    if not os.path.exists(schema_path):
        raise FileNotFoundError(f"Schema file not found: {schema_path}")

    conn = get_connection()
    try:
        with open(schema_path, "r") as f:
            sql = f.read()
        conn.executescript(sql)
        conn.commit()
        print(f"Schema applied from {schema_path}")
    finally:
        conn.close()

if __name__ == "__main__":
    run_schema()
    # optional seed
    try:
        from lib.db.seed import seed
        seed()
        print("Seeded data.")
    except Exception as e:
        print("Seed failed:", e)
