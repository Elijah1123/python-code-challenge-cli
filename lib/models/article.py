# lib/models/article.py
import os
import sys
from typing import Optional

# ✅ Ensure project root is on sys.path (like seed.py)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from lib.db.connection import get_connection


class Article:
    def __init__(self, title: str, author_id: int, magazine_id: int, id: Optional[int] = None):
        if not title or not title.strip():
            raise ValueError("Article title required")
        self.id = id
        self.title = title.strip()
        self.author_id = author_id
        self.magazine_id = magazine_id

    def __repr__(self):
        return f"<Article {self.id}: {self.title} (author {self.author_id}, mag {self.magazine_id})>"

    def save(self):
        conn = get_connection()
        try:
            cur = conn.cursor()
            if self.id:
                cur.execute(
                    "UPDATE articles SET title = ?, author_id = ?, magazine_id = ? WHERE id = ?",
                    (self.title, self.author_id, self.magazine_id, self.id),
                )
            else:
                cur.execute(
                    "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                    (self.title, self.author_id, self.magazine_id),
                )
                self.id = cur.lastrowid
            conn.commit()
            return self
        finally:
            conn.close()

    @classmethod
    def find_by_id(cls, aid: int):
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM articles WHERE id = ?", (aid,))
            row = cur.fetchone()
            return cls(row["title"], row["author_id"], row["magazine_id"], row["id"]) if row else None
        finally:
            conn.close()

    @classmethod
    def find_by_title(cls, title: str):
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM articles WHERE title = ?", (title.strip(),))
            rows = cur.fetchall()
            return [cls(r["title"], r["author_id"], r["magazine_id"], r["id"]) for r in rows]
        finally:
            conn.close()

    @classmethod
    def find_by_author(cls, author_id: int):
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM articles WHERE author_id = ?", (author_id,))
            rows = cur.fetchall()
            return [cls(r["title"], r["author_id"], r["magazine_id"], r["id"]) for r in rows]
        finally:
            conn.close()

    @classmethod
    def find_by_magazine(cls, magazine_id: int):
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM articles WHERE magazine_id = ?", (magazine_id,))
            rows = cur.fetchall()
            return [cls(r["title"], r["author_id"], r["magazine_id"], r["id"]) for r in rows]
        finally:
            conn.close()
