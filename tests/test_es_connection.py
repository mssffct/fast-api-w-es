import pytest

from app.main import es


@pytest.fixture
def es_client():
    return es


def test_connection(es_client):
    assert es_client.ping() is True
