from dataclasses import dataclass


@dataclass
class Station:
    id: str
    name: str
    longitude: float
    latitude: float
