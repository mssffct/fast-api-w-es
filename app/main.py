import os
from typing import Optional

from dotenv import find_dotenv, load_dotenv
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
from fastapi import FastAPI, HTTPException, Path, status
from fastapi.encoders import jsonable_encoder

from app.schemas import SearchOption, TextPiece, TextPieceType

load_dotenv(find_dotenv())
INDEX_TAG = "Indexing"
SEARCH_TAG = "Searching"
SAVE_PATH = "/save"
SEARCH_PATH = "/search"
ES_PORT = os.environ.get("ES_PORT")

tags = [
    {
        "name": INDEX_TAG,
        "description": "Saving text pieces.",
    },
    {
        "name": SEARCH_TAG,
        "description": "Searching among already saved results with optional filter usage.",
    },
]

app = FastAPI(
    title="fast-api-w-es",
    openapi_tags=tags,
)
es = Elasticsearch([f"localhost:{ES_PORT}"])


@app.post(
    SAVE_PATH + "/{text_type}",
    status_code=status.HTTP_201_CREATED,
    response_model=TextPiece,
    summary="Save text piece.",
    tags=[INDEX_TAG],
)
def save_text_piece(
    text_piece: TextPiece,
    text_type: str = Path(..., example="paragraph"),
):
    text_piece_data = jsonable_encoder(text_piece)
    index_name = text_piece.doc_name.split(".")[0]
    try:
        res = es.search(
            index=index_name,
            query={
                "bool": {
                    "must": [
                        {"match": {"text": text_piece.text}},
                        {"match": {"text_type": text_piece.text_type}},
                        {"match": {"page_number": text_piece.page_number}},
                    ]
                }
            },
        )
        if res["hits"]["total"] > 0:
            raise HTTPException(status_code=400, detail=f"Text sample already exists. ")
            pass
        else:
            if text_piece.text:
                es.index(index=index_name, document=text_piece_data)
            else:
                raise HTTPException(
                    status_code=400, detail=f"Can't save empty text piece. "
                )
                pass
    except NotFoundError:
        es.index(index=index_name, document=text_piece_data)


@app.get(
    SEARCH_PATH + "/{option}/{user_filter}",
    summary="Search text pieces with filter usage. ",
    tags=[SEARCH_TAG],
)
def search_text_piece(
    option: SearchOption,
    text_piece_type: Optional[TextPieceType] = None,
    text_sample: Optional[str] = None,
    doc_name: Optional[str] = None,
    page_number: Optional[int] = None,
):
    index_name = doc_name.split(".")[0]
    if (
        option == SearchOption.search_definite
        and (doc_name and page_number)
        and not text_sample
    ):
        try:
            res = es.search(
                index=index_name, query={"match": {"page_number": page_number}}
            )
            return res["hits"]
        except NotFoundError:
            raise HTTPException(
                status_code=400,
                detail=f"Document with name: {doc_name} hasn't been validated yet. ",
            )
    elif option == SearchOption.search_by_type and not (
        doc_name or page_number or text_sample
    ):
        indexes = es.indices.get_alias().keys()
        result = []
        for index in indexes:
            res = es.search(
                index=index, query={"match": {"text_type": text_piece_type}}
            )
            result.append(res["hits"]["hits"])
        return result
    elif option == SearchOption.search_similar and not (doc_name or page_number):
        indexes = es.indices.get_alias().keys()
        result = []
        for index in indexes:
            res = es.search(
                index=index,
                query={
                    "bool": {
                        "must": [
                            {
                                "match": {
                                    "text": {"query": text_sample, "fuzziness": "auto"}
                                }
                            },
                            {"match": {"text_type": text_piece_type}},
                        ]
                    }
                },
            )
            if res["hits"]["total"] > 0:
                result.append(res["hits"]["hits"])
            else:
                pass
        return result
    elif (
        option == SearchOption.mixed
        and doc_name
        and text_piece_type
        and not text_sample
    ):
        res = es.search(index=index_name, query={"match": {"text_type": text_piece_type}})
        return res
    elif option == SearchOption.mixed and doc_name and text_sample and text_piece_type:
        res = es.search(
            index=index_name,
            query={
                "bool": {
                    "must": [
                        {
                            "match": {
                                "text": {"query": text_sample, "fuzziness": "auto"}
                            }
                        },
                        {"match": {"text_type": text_piece_type}},
                    ]
                }
            },
        )
        return res
    elif (
        option == SearchOption.mixed
        and doc_name
        and text_sample
        and not text_piece_type
    ):
        res = es.search(
            index=index_name,
            query={"match": {"text": {"query": text_sample, "fuzziness": "auto"}}},
        )
        return res
    else:
        raise HTTPException(
            status_code=400, detail="Please specify correct search params"
        )
