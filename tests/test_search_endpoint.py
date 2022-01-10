import pytest
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
        doc_name="test_1.pdf",
    )
    index_name = text_piece.doc_name.split(".")[0]
    return text_piece, index_name


def test_search_definite(text_piece_obj):
    res = es.search(
        index=text_piece_obj[1],
        body={"query": {"match": {"page_number": text_piece_obj[0].page_number}}},
    )
    assert res["hits"]["total"] > 0


def test_search_definite_not_validated_doc():
    response = client.get(
        f"search/definite", params={"doc_name": "0", "page_number": 1}
    )
    assert response.status_code == 404


def test_search_by_type(text_piece_obj):
    res = es.search(
        index=text_piece_obj[1],
        body={"query": {"match": {"text_type": text_piece_obj[0].text_type}}},
    )
    assert res["hits"]["total"] > 0


def test_search_similar(text_piece_obj):
    res = es.search(
        index=text_piece_obj[1],
        body={
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "text": {"query": "some new tet", "fuzziness": "auto"}
                            }
                        },
                        {"match": {"text_type": text_piece_obj[0].text_type}},
                    ]
                }
            }
        },
    )
    assert res["hits"]["total"] > 0


def test_mixed_search_with_doc_name_and_type(text_piece_obj):
    res = es.search(
        index=text_piece_obj[1],
        body={
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "text": {"query": "some new tet", "fuzziness": "auto"}
                            }
                        },
                        {"match": {"text_type": text_piece_obj[0].text_type}},
                    ]
                }
            }
        },
    )
    assert res["hits"]["total"] > 0


def test_mixed_search_with_doc_name_and_sample(text_piece_obj):
    res = es.search(
        index=text_piece_obj[1],
        body={
            "query": {"match": {"text": {"query": "some new tet", "fuzziness": "auto"}}}
        },
    )
    assert res["hits"]["total"] > 0


def test_not_valid_parameters_given():
    response = client.get(f"search/definite", params={})
    assert response.status_code == 404
