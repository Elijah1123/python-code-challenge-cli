# lib/db/connection.py
import os
import sqlite3

# Project root (two levels up from this file: lib/db -> lib -> project root)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DB_PATH = os.getenv("DB_PATH", os.path.join(PROJECT_ROOT, "articles.db"))

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
