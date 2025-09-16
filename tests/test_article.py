# tests/test_article.py
from lib.models.article import Article
from lib.models.author import Author
from lib.models.magazine import Magazine

def test_article_crud():
    a = Author("ArtAuthor"); a.save()
    m = Magazine("ArtMag", "Art"); m.save()

    art = Article("Art Title", a.id, m.id)
    art.save()
    assert art.id is not None

    fetched = Article.find_by_id(art.id)
    assert fetched.title == "Art Title"

    by_author = Article.find_by_author(a.id)
    assert any(x.title == "Art Title" for x in by_author)

    by_mag = Article.find_by_magazine(m.id)
    assert any(x.title == "Art Title" for x in by_mag)
