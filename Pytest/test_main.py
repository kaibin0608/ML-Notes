# We write unit test to :
# 1. check if our code is working as expected
# 2. if we make changes to our code in future, we can run the tests
# 3. if we do get an error: we can quickly identify where the problem is and fix it very easily

import pytest
from main import divide,add
from main import get_weather

def test_get_weather():
    # assert is going to tell us something is true or false
    assert get_weather(21) == "cold"
    assert get_weather(15) == "cold"

def test_add():
    assert add(2,3) == 5, "2 + 3 should be 5"
    assert add(-1,1) == 0, " -1 + 1 should be 0"
    assert add(0,0) == 0, " 0 + 0 should be 0"

def test_divide():
    with pytest.raises(ZeroDivisionError, match="can by zero is not allowed."):
        divide(10,0)
    # assert divide(6,3) == 2, "6 / 3 should be 2"
    # assert divide(-4,2) == -2, "-4 / 2 should be -2"

from main import UserManager

# fixture is something that you can have run before every single test
# it is like a setup method that runs before every test to set up a fresh instance to inject this fixture into our test function
# so every time the test function runs, we get a fresh instance of UserManager, this is important because 
# if we use the same instance across multiple tests, the state from one test could affect another test leading to unreliable results
@pytest.fixture 
def user_manager():
    """Creates a fresh instance of UserManager before each test."""
    return UserManager()

# if we dont use fixture, the second test will fail because the user "john_doe" already added from the first test
# user_manager = UserManager()

def test_add_user(user_manager):
    assert user_manager.add_user("john_doe","john@example.com") == True
    assert user_manager.get_user("john_doe") == "john@example.com"

def test_add_duplicate_user(user_manager):
    user_manager.add_user("john_doe","john@example.com")
    with pytest.raises(ValueError):
        user_manager.add_user("john_doe","another@example.com")

from main import Database

@pytest.fixture
def db():
    """Provides a fresh instance of te Database class for testing and clean up after the test."""
    database = Database()
    yield database  # Provide the database instance to the test
    # Teardown code: Clean up after the test
    database.data.clear() # as soon as the test is done, this code runs to clear the database

def test_add_user(db):
    db.add_user(1, "Alice")
    assert db.get_user(1) == "Alice"

def test_add_duplicate_user(db):
    db.add_user(1, "Alice")
    with pytest.raises(ValueError, match = "User already exists"):
        db.add_user(1, "Bob")

def test_delete_user(db):
    db.add_user(2, "Bob")
    db.delete_user(2)
    assert db.get_user(2) is None


from main import is_prime

@pytest.mark.parameterize("num, expected",[
    (1, False),
    (2, False),
    (3, True),
    (4, False),
    (5, True),
    (16, False),
    (17, True),
    (18, False),
    (19, True),
])
def test_is_prime(num, expected):
    assert is_prime(num) == expected