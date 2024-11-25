from fastapi import FastAPI, Query
from dto import TableSearchDto
from embedder import Embedder
import pymilvus as pm
import searcher
import time

try:
    pm.connections.connect("default", host="localhost", port="19530")
    print("Connection successful!")
except pm.exceptions.MilvusException as e:
    print(f"Failed to connect to Milvus: {e}")
    exit()
    
app = FastAPI()

@app.get("/api/table/search", response_model=TableSearchDto)
def get_tables(
    query: str, 
    paper_ids: list[str] = Query(), 
    model_name: str = Query("distilbert-base-uncased"), 
    method_name: str = Query("tab_cap_embedding"),
    number_of_results: int = Query(50),
    use_hybrid: bool = Query(True),
    use_groud_truth: bool = Query(False)):

    print(query, paper_ids)

    embedder = Embedder(model_name=model_name)

    start_time = time.time() * 1000
    
    searcher.search(query, embedder, method_name, number_of_results, paper_ids, use_hybrid, use_groud_truth)

    elapsed_time = (time.time() - start_time) * 1000

    response = TableSearchDto(
        tables=[],
        suggestion=query,
        queryTimeMs=elapsed_time
    )

    return response

# run with uvicorn app:app --reload --port 8000