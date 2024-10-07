class TableSchema(dict):
    caption: str
    table: str
    footnotes: list[str]
    references: list[str]
    