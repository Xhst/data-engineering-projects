from pydantic import BaseModel


class TableDto(BaseModel):
    paperId: str
    tableId: str
    score: float
    

class TableSearchDto(BaseModel):
    tables: list[TableDto]
    suggestion: str
    queryTimeMs: float