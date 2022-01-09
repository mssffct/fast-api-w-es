from enum import Enum

from pydantic import BaseModel, Field


class TextPieceType(str, Enum):
    title = "title"
    paragraph = "paragraph"


class TextPiece(BaseModel):
    text: str = Field(..., example="saved text piece")
    text_type: TextPieceType = Field(..., example=TextPieceType.paragraph)
    page_number: int = Field(..., ge=1, example=2)
    doc_name: str = Field(..., example="source_document_name.pdf")


class SearchOption(str, Enum):
    search_by_type = "by_type"
    search_similar = "similar"
    search_definite = "definite"
    mixed = "mixed"
