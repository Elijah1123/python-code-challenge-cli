# lib/models/author.py
import os
import sys
from typing import List, Optional

# ✅ Ensure project root is on sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from lib.db.connection import get_connection

# lib/models/magazine.py
from typing import List, Optional
from lib.db.connection import get_connection

class Magazine:
    def __init__(self, name: str, category: str, id: Optional[int] = None):
        if not name or not name.strip():
            raise ValueError("Magazine name required")
        if not category or not category.strip():
            raise ValueError("Magazine category required")
        self.id = id
        self.name = name.strip()
        self.category = category.strip()

    def __repr__(self):
        return f"<Magazine {self.id}: {self.name} ({self.category})>"

    def save(self):
        conn = get_connection()
        try:
            cur = conn.cursor()
            if self.id:
                cur.execute("UPDATE magazines SET name = ?, category = ? WHERE id = ?", (self.name, self.category, self.id))
            else:
                cur.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (self.name, self.category))
                self.id = cur.lastrowid
            conn.commit()
            return self
        finally:
            conn.close()

    @classmethod
    def find_by_id(cls, mid: int):
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM magazines WHERE id = ?", (mid,))
            row = cur.fetchone()
            return cls(row["name"], row["category"], row["id"]) if row else None
        finally:
            conn.close()

    @classmethod
    def find_by_name(cls, name: str):
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM magazines WHERE name = ?", (name.strip(),))
            row = cur.fetchone()
            return cls(row["name"], row["category"], row["id"]) if row else None
        finally:
            conn.close()

    @classmethod
    def find_by_category(cls, category: str):
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM magazines WHERE category = ?", (category.strip(),))
            rows = cur.fetchall()
            return [cls(r["name"], r["category"], r["id"]) for r in rows]
        finally:
            conn.close()

    def articles(self):
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM articles WHERE magazine_id = ?", (self.id,))
            return cur.fetchall()
        finally:
            conn.close()

    def contributors(self):
        """
        Unique list of authors (rows) who wrote for this magazine.
        """
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT DISTINCT au.* FROM authors au
                JOIN articles a ON au.id = a.author_id
                WHERE a.magazine_id = ?
            """, (self.id,))
            return cur.fetchall()
        finally:
            conn.close()

    def article_titles(self):
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT title FROM articles WHERE magazine_id = ?", (self.id,))
            return [r["title"] for r in cur.fetchall()]
        finally:
            conn.close()

    def contributing_authors(self, threshold=2):
        """
        Returns authors who have more than `threshold` articles in this magazine.
        """
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT au.*, COUNT(a.id) as cnt
                FROM authors au
                JOIN articles a ON au.id = a.author_id
                WHERE a.magazine_id = ?
                GROUP BY au.id
                HAVING cnt > ?
            """, (self.id, threshold))
            return cur.fetchall()
        finally:
            conn.close()

    @classmethod
    def top_publisher(cls):
        """
        Magazine with the most articles.
        """
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT m.*, COUNT(a.id) as cnt
                FROM magazines m
                LEFT JOIN articles a ON m.id = a.magazine_id
                GROUP BY m.id
                ORDER BY cnt DESC
                LIMIT 1
            """)
            row = cur.fetchone()
            return cls(row["name"], row["category"], row["id"]) if row else None
        finally:
            conn.close()

    @classmethod
    def magazines_with_at_least_two_authors(cls):
        """
        Magazines that have articles by at least 2 different authors.
        """
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT m.* FROM magazines m
                JOIN articles a ON m.id = a.magazine_id
                GROUP BY m.id
                HAVING COUNT(DISTINCT a.author_id) >= 2
            """)
            rows = cur.fetchall()
            return [cls(r["name"], r["category"], r["id"]) for r in rows]
        finally:
            conn.close()
