
import pytest

from wqet_grader.server import app

@pytest.fixture
def http_client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
