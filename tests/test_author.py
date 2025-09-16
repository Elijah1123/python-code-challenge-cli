# tests/test_author.py
import pytest
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

def test_author_create_and_find():
    a = Author("Tester")
    a.save()
    assert a.id is not None

    found = Author.find_by_id(a.id)
    assert found.name == "Tester"

def test_add_article_and_relations():
    # create magazine
    m = Magazine("Test Mag", "Testing")
    m.save()
    a = Author("Writer")
    a.save()

    art_id = a.add_article(m, "Breaking Tests")
    assert art_id is not None

    arts = a.articles()
    assert any(r["id"] == art_id for r in arts)

    mags = a.magazines()
    assert any(r["id"] == m.id for r in mags)

def test_add_author_with_articles_transaction():
    # create magazine to reference
    m = Magazine("Trans Mag", "Trans")
    m.save()
    articles_data = [
        {"title": "One", "magazine_id": m.id},
        {"title": "Two", "magazine_id": m.id},
    ]
    author = Author.add_author_with_articles("TranAuthor", articles_data)
    assert author.id is not None

def test_most_prolific():
    # ensure function runs (seeded data might make Alice most prolific)
    top = Author.most_prolific()
    assert top is not None
