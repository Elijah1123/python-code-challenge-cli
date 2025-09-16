# tests/conftest.py
import os
import shutil
import tempfile
import pytest

TEST_DB = "test_articles.db"

@pytest.fixture(autouse=True, scope="session")
def prepare_test_db():
    # Ensure clean DB file
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    os.environ["DB_PATH"] = TEST_DB
    # run schema & seed
    from lib.db.connection import get_connection
    conn = get_connection()
    try:
        with open("lib/db/schema.sql", "r") as f:
            conn.executescript(f.read())
        conn.commit()
    finally:
        conn.close()
    yield
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
