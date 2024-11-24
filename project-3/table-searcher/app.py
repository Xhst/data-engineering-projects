from fastapi import FastAPI, Query
from dto import TableSearchDto
from embedder import Embedder
import searcher
import time

app = FastAPI()

@app.get("/api/table/search", response_model=TableSearchDto)
def get_tables(
    query: str, 
    paper_ids: list[str] = Query(), 
    model_name: str = Query("distilbert-base-uncased"), 
    method_name: str = Query("tab_cap_embedding"),
    use_hybrid: bool = Query(False)):

    print(query, paper_ids)

    embedder = Embedder(model_name=model_name)

    start_time = time.time()
    
    searcher.search(query, embedder, method_name, paper_ids, use_hybrid)

    elapsed_time = time.time() - start_time

    response = TableSearchDto(
        tables=[],
        suggestion=query,
        queryTimeMs=elapsed_time
    )

    return response

# run with uvicorn app:app --reload --port 8000