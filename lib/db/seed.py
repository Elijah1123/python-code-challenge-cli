# lib/db/seed.py
import os
import sys

# If script is run directly, ensure project root is on sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from lib.db.connection import get_connection

def seed():
    conn = get_connection()
    try:
        cur = conn.cursor()

        # ✅ Ensure schema exists before seeding
        schema_path = os.path.join(PROJECT_ROOT, "lib", "db", "schema.sql")
        with open(schema_path, "r") as f:
            cur.executescript(f.read())

        # Insert authors
        authors = ["Alice Walker", "Bob Smith", "Carol Jones"]
        for name in authors:
            cur.execute("INSERT OR IGNORE INTO authors (name) VALUES (?)", (name,))
        print(f"Inserted {len(authors)} authors (or ignored duplicates).")

        # Insert magazines
        mags = [
            ("Tech Monthly", "Technology"),
            ("Health Weekly", "Health"),
            ("Travel Today", "Travel"),
        ]
        for name, cat in mags:
            cur.execute(
                "INSERT OR IGNORE INTO magazines (name, category) VALUES (?, ?)",
                (name, cat),
            )
        print(f"Inserted {len(mags)} magazines (or ignored duplicates).")

        # Fetch IDs
        cur.execute("SELECT id, name FROM authors")
        authors_map = {row["name"]: row["id"] for row in cur.fetchall()}
        cur.execute("SELECT id, name FROM magazines")
        mags_map = {row["name"]: row["id"] for row in cur.fetchall()}

        # Insert articles
        articles = [
            ("AI and You", authors_map["Alice Walker"], mags_map["Tech Monthly"]),
            ("Healthy Eating", authors_map["Bob Smith"], mags_map["Health Weekly"]),
            ("The Nairobi Guide", authors_map["Carol Jones"], mags_map["Travel Today"]),
            ("Deep Learning", authors_map["Alice Walker"], mags_map["Tech Monthly"]),
            ("Remote Work Trends", authors_map["Bob Smith"], mags_map["Tech Monthly"]),
            ("Travel on Budget", authors_map["Alice Walker"], mags_map["Travel Today"]),
            ("Wellness Tips", authors_map["Carol Jones"], mags_map["Health Weekly"]),
        ]
        for title, author_id, magazine_id in articles:
            cur.execute(
                "INSERT OR IGNORE INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                (title, author_id, magazine_id),
            )
        print(f"Inserted {len(articles)} articles (or ignored duplicates).")

        conn.commit()
        print("✅ Database seeded successfully.")
    finally:
        conn.close()

if __name__ == "__main__":
    seed()
