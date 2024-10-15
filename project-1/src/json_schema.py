from dataclasses import dataclass, field

@dataclass
class TableData:
    caption: str = ""
    table: str = ""
    footnotes: list[str] = field(default_factory=list)
    references: list[str] = field(default_factory=list)