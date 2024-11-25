from index_schema import schema
from embedder import Embedder
from dto import TableDto
from indexer import get_collection_name
import pymilvus as pm


def search(query: str, embedder: Embedder, function_name: str, number_of_results: int, paper_ids: list[str], use_hybrid: bool, use_ground_truth: bool) -> list[TableDto]:
    tables_dto: list[TableDto] = []
    
    query_vector = embedder.get_sentence_embedding(query).tolist()

    search_params = {"metric_type": "COSINE", "params": {"nprobe": 200}}

    collection_name = get_collection_name(embedder, function_name, use_ground_truth)
    
    collection = pm.Collection(name=collection_name, schema=schema)
    
    collection.load()

    results = collection.search(
        data=[query_vector],
        anns_field="vector",
        param=search_params,
        limit=number_of_results,
        output_fields=["id", "paper_id", "table_id"]
    )

    for hits in results:
        for hit in hits:
            if not use_hybrid or (hit.entity.get('paper_id') in paper_ids):
                dto = TableDto(
                    paperId=hit.entity.get('paper_id'),
                    tableId=hit.entity.get('table_id'),
                    score=hit.distance)
                tables_dto.append(dto)

    return tables_dto