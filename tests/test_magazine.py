# tests/test_magazine.py
from lib.models.magazine import Magazine
from lib.models.author import Author
from lib.models.article import Article

def test_magazine_create_and_find():
    m = Magazine("MTest", "Cat")
    m.save()
    assert m.id is not None
    found = Magazine.find_by_id(m.id)
    assert found.name == "MTest"

def test_contributors_and_titles_and_contributing_authors():
    a1 = Author("C1"); a1.save()
    a2 = Author("C2"); a2.save()
    m = Magazine("ContribMag", "TestCat"); m.save()

    a1.add_article(m, "A1")
    a1.add_article(m, "A1-2")
    a1.add_article(m, "A1-3")
    a2.add_article(m, "A2-1")

    titles = m.article_titles()
    assert "A1" in titles

    contributors = m.contributors()
    assert any(c["name"] == "C1" for c in contributors)
    contributing_authors = m.contributing_authors(threshold=2)
    assert any(c["name"] == "C1" for c in contributing_authors)
