import time

import pytest
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient

from app.main import app, es
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
    response = client.post(f"save/{text_piece_obj.text_type}", json=data_to_save)
    assert response.status_code == 201


def test_text_piece_already_exists(text_piece_obj):
    time.sleep(3)
    index_name = text_piece_obj.doc_name.split(".")[0]
    res = es.search(
        index=index_name,
        body={
            "query": {
                "bool": {
                    "must": [
                        {"match": {"text": text_piece_obj.text}},
                        {"match": {"text_type": text_piece_obj.text_type}},
                        {"match": {"page_number": text_piece_obj.page_number}},
                    ]
                }
            }
        },
    )
    assert res["hits"]["total"] > 0


def test_empty_text_piece_given():
    response = client.post(
        f"save/title",
        json={
            "text": "",
            "text_type": "title",
            "page_number": 1,
            "doc_name": "test_doc2.pdf",
        },
    )
    assert response.status_code == 400
