import pymilvus as pm
from embedder import Embedder

def getField(embedder: Embedder):
    return [
        pm.FieldSchema(name="id", dtype=pm.DataType.VARCHAR, is_primary=True, max_length=128),
        pm.FieldSchema(name="paper_id", dtype=pm.DataType.VARCHAR, is_primary=False, max_length=32),
        pm.FieldSchema(name="table_id", dtype=pm.DataType.VARCHAR, is_primary=False, max_length=96),
        pm.FieldSchema(name="vector", dtype=pm.DataType.FLOAT_VECTOR, dim=embedder.embedding_size, is_primary=False)
    ]

def get_schema(embedder: Embedder):
    fields = getField(embedder)
    return pm.CollectionSchema(fields=fields, description="Table Searcher Collection")