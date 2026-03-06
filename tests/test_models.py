import pytest
from vainamoinen import db, create_app
from vainamoinen.Database import User

@pytest.fixture
def db_handle():
    config = {
        "SQLALCHEMY_DATABASE_URI": "sqlite:///test.db",
        "TESTING": True,
        "CACHE_TYPE": "SimpleCache"
    }

    app = create_app(config)

    ctx = app.app_context()
    ctx.push()

    db.create_all()
    yield db

    db.session.rollback()
    db.drop_all()
    db.session.remove()
    ctx.pop()


def _get_user(number):
    '''
    Creates a valid user object to be used for DB tests.
    '''

    return User(
        username = "test-user-{}".format(number),
        password = "1234",
        email = "email{}.com".format(number),
        address = "Test Street 1",
        phone_number = "123 456 7890",
        description = "This is a Test User"
    )


def test_add_user(db_handle):
    '''
    Test adding 1 new user
    '''
    user = _get_user(1)
    db_handle.session.add(user)
    db_handle.session.commit()

    assert User.query.count() == 1


# Database test here:
