from typing import TypedDict, List

class TableSchema(TypedDict):
    caption: str
    table: str
    footnotes: List[str]
    references: List[str]
    