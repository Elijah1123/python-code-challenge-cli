# lib/models/author.py
import os
import sys
from typing import List, Optional

# ✅ Ensure project root is on sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from lib.db.connection import get_connection

# lib/models/author.py
from typing import List, Optional
from lib.db.connection import get_connection

class Author:
    def __init__(self, name: str, id: Optional[int] = None):
        if not name or not name.strip():
            raise ValueError("Author name must be provided")
        self.id = id
        self.name = name.strip()

    def __repr__(self):
        return f"<Author {self.id}: {self.name}>"

    def save(self):
        conn = get_connection()
        try:
            cur = conn.cursor()
            if self.id:
                cur.execute("UPDATE authors SET name = ? WHERE id = ?", (self.name, self.id))
            else:
                cur.execute("INSERT INTO authors (name) VALUES (?)", (self.name,))
                self.id = cur.lastrowid
            conn.commit()
            return self
        finally:
            conn.close()

    @classmethod
    def find_by_id(cls, author_id: int):
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM authors WHERE id = ?", (author_id,))
            row = cur.fetchone()
            return cls(row["name"], row["id"]) if row else None
        finally:
            conn.close()

    @classmethod
    def find_by_name(cls, name: str):
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM authors WHERE name = ?", (name.strip(),))
            row = cur.fetchone()
            return cls(row["name"], row["id"]) if row else None
        finally:
            conn.close()

    def articles(self):
        """
        Returns list of sqlite3.Row for articles written by this author.
        """
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM articles WHERE author_id = ?", (self.id,))
            return cur.fetchall()
        finally:
            conn.close()

    def magazines(self):
        """
        Returns distinct magazines (rows) this author has contributed to.
        """
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT DISTINCT m.* FROM magazines m
                JOIN articles a ON m.id = a.magazine_id
                WHERE a.author_id = ?
            """, (self.id,))
            return cur.fetchall()
        finally:
            conn.close()

    def topic_areas(self):
        """
        Unique categories of magazines this author has contributed to.
        """
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT DISTINCT m.category FROM magazines m
                JOIN articles a ON m.id = a.magazine_id
                WHERE a.author_id = ?
            """, (self.id,))
            return [r["category"] for r in cur.fetchall()]
        finally:
            conn.close()

    def add_article(self, magazine, title: str):
        """
        magazine: either a Magazine instance or an integer magazine_id
        """
        if not title or not title.strip():
            raise ValueError("Article title must be provided")
        mag_id = magazine.id if hasattr(magazine, "id") else magazine
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                (title.strip(), self.id, mag_id)
            )
            conn.commit()
            return cur.lastrowid
        finally:
            conn.close()

    @classmethod
    def add_author_with_articles(cls, author_name: str, articles_data: list):
        """
        Transaction: add author and their articles atomically.
        articles_data: list of dicts {'title': str, 'magazine_id': int}
        Returns Author instance on success, raises on failure.
        """
        conn = get_connection()
        try:
            cur = conn.cursor()
            conn.execute("BEGIN")
            cur.execute("INSERT INTO authors (name) VALUES (?)", (author_name.strip(),))
            author_id = cur.lastrowid

            for a in articles_data:
                if "title" not in a or "magazine_id" not in a:
                    raise ValueError("Each article must have 'title' and 'magazine_id'")
                cur.execute(
                    "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                    (a["title"].strip(), author_id, a["magazine_id"])
                )
            conn.commit()
            return cls(author_name, author_id)
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @classmethod
    def most_prolific(cls):
        """
        Returns the author row with the most articles (if tie, returns one of them).
        """
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT au.*, COUNT(a.id) as cnt
                FROM authors au
                LEFT JOIN articles a ON au.id = a.author_id
                GROUP BY au.id
                ORDER BY cnt DESC
                LIMIT 1
            """)
            row = cur.fetchone()
            return cls(row["name"], row["id"]) if row else None
        finally:
            conn.close()
