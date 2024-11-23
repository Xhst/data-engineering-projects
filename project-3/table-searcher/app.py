from fastapi import FastAPI, Query
from pydantic import BaseModel
import time

app = FastAPI()

class TableDto(BaseModel):
    paperId: str
    tableId: str
    score: float
    

class TableSearchDto(BaseModel):
    tables: list[TableDto]
    suggestion: str
    queryTimeMs: int


@app.get("/api/table/search", response_model=TableSearchDto)
def get_tables(query: str, paper_ids: list[str] = Query(...)):

    print(query, paper_ids)

    start_time = time.time()

    elapsed_time = time.time() - start_time

    response = TableSearchDto(
        tables=[],
        suggestion=query,
        queryTimeMs=elapsed_time
    )

    return response

# docker run -d --name milvus-standalone -p 19530:19530 -p 9091:9091 milvusdb/milvus:latest

# run with uvicorn app:app --reload --port 8000