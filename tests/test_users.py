from models.users import Admin, Author, hash_password


def test_admin_and_author_permissions():
    admin = Admin(1, "Admin", "admin", hash_password("secret"))
    author = Author(2, "Author", "author", hash_password("secret"))
    assert admin.can_edit
    assert not author.can_edit


def test_password_verification():
    user = Author(2, "Author", "author", hash_password("secret"))
    assert user.verify_password("secret")
    assert not user.verify_password("wrong")
