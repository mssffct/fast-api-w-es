import pytest
import requests
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient

from app.main import app
from app.schemas import TextPiece, TextPieceType

client = TestClient(app)


@pytest.fixture
def text_piece_obj():
    text_piece = TextPiece(
        text="some new text",
        text_type=TextPieceType.title,
        page_number=1,
        doc_name="test_7.pdf",
    )
    return text_piece


def test_index_creation(text_piece_obj):
    data_to_save = jsonable_encoder(text_piece_obj)
    response = client.post("/text", json=data_to_save)
    assert response.status_code == 201


def test_search_all(text_piece_obj):
    response = client.get("/text")
    assert response.status_code == 200
    assert response.json() == text_piece_obj


def test_search_by_filter_text_sample(text_piece_obj):
    parameters = {"text_sample": "some new te"}
    response = client.get("/text", params=parameters)
    assert response.status_code == 200
    assert response.json() == text_piece_obj


def test_search_by_filter_various_parameters(text_piece_obj):
    parameters = {
        "text_piece_type": "title",
        "doc_name": text_piece_obj.doc_name,
        "page_number": text_piece_obj.page_number
    }
    response = client.get("/text", params=parameters)
    assert response.status_code == 200
    assert response.json() == text_piece_obj
