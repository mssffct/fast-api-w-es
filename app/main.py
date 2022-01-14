from typing import Optional

from fastapi import FastAPI, Query, status
from fastapi.encoders import jsonable_encoder

from app.schemas import TextPiece, TextPieceType
from app.es_handler import (
    text_piece_indexer,
    search_all,
    search_by_filter
)


INDEX_TAG = "Indexing"
SEARCH_TAG = "Searching"
TEXT_PATH = "/text"

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


@app.post(
    TEXT_PATH,
    status_code=status.HTTP_201_CREATED,
    response_model=TextPiece,
    summary="Save text piece.",
    tags=[INDEX_TAG],
)
def index_text_piece(
    text_piece: TextPiece,
):
    text_piece_data = jsonable_encoder(text_piece)
    return text_piece_indexer(text_piece_data)


@app.get(
    TEXT_PATH,
    summary="Search text pieces with filter usage. ",
    tags=[SEARCH_TAG],
)
def search_text_piece(
    text_piece_type: Optional[TextPieceType] = Query(
        None, description="Finds titles or paragraphs"
    ),
    text_sample: Optional[str] = Query(
        None, example="Text i want to find",
        description="Finds similarities"
    ),
    doc_name: Optional[str] = Query(
        None, example="MyDocument"
    ),
    page_number: Optional[int] = Query(
        None, example=2
    ),
):
    args = (text_piece_type, text_sample, doc_name, page_number)
    arg_names = (
        "text_piece_type", "text_sample", "doc_name", "page_number"
    )
    if any(args):
        parameters = {name: item for item, name in zip(args, arg_names) if item}
        return search_by_filter(parameters)
    else:
        return search_all()
