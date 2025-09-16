
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
# scripts/run_queries.py
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.connection import get_connection


def example():
    # List all articles by author Alice Walker
    alice = Author.find_by_name("Alice Walker")
    if alice:
        print("Alice's articles:")
        for a in alice.articles():
            print(" -", a["title"])

    # Magazines Alice has contributed to
    print("Alice's magazines:")
    for m in alice.magazines():
        print(" -", m["name"], "(", m["category"], ")")

    # Top publisher
    top = Magazine.top_publisher()
    print("Top publisher:", top)

    # Magazines with >= 2 different authors
    mags = Magazine.magazines_with_at_least_two_authors()
    print("Magazines with articles by >=2 authors:", mags)

if __name__ == "__main__":
    example()
