from dataclasses import dataclass, field


@dataclass
class Line:
    id: int = field(repr=False)
    name: str
