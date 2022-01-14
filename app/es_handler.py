import os
from typing import Union, Set
from dotenv import find_dotenv, load_dotenv
from elasticsearch import Elasticsearch


load_dotenv(find_dotenv())

ES_HOST = os.environ.get("ES_HOST")
ES_PORT = os.environ.get("ES_PORT")
ES_INDEX = os.environ.get("ES_INDEX")

es = Elasticsearch([f"{ES_HOST}:{ES_PORT}"])


def text_piece_indexer(text_piece: dict) -> None:
    """
    Indexes TextPiece object
    :param text_piece: TextPiece object
    :return: None
    """
    es.index(index=ES_INDEX, doc_type="doc", body=text_piece)


def search_all() -> Union[Set[dict], str]:
    """
    Returns all text pieces
    :return: set of results
    """
    results = es.search(index=ES_INDEX, body={"query": {"bool": {"must": []}}})
    return set(item["_source"] for item in results["hits"]["hits"])


def search_by_filter(parameters: dict) -> Union[Set[dict], str]:
    """
    Returns all text pieces of definite document's page
    :param parameters: dict of specified parameters
    :return: set of results
    """
    query = {"query": {"bool": {"must": []}}}
    search_text = parameters.get("text_sample")
    if search_text:
        query["query"]["bool"]["must"].append(
            {"match": {"text": {"query": search_text, "fuzziness": "auto"}}}
        )
    else:
        for key, value in parameters.items():
            query["query"]["bool"]["must"].append({"match": {key: value}})
    results = es.search(index=ES_INDEX, body=query)
    return set(item["_source"] for item in results["hits"]["hits"])
