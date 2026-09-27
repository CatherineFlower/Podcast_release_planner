from models.podcasts import add_podcast, find_podcasts
from models.users import Author, hash_password


def test_add_podcast():
    author = Author(2, "Author", "author", hash_password("x"))
    podcasts = []
    podcast = add_podcast(podcasts, "Test", "Description", author)
    assert podcast.id == 1
    assert podcast.author is author


def test_find_podcasts():
    author = Author(2, "Author", "author", hash_password("x"))
    podcasts = []
    add_podcast(podcasts, "Python Talks", "Description", author)
    assert len(find_podcasts(podcasts, "python")) == 1
