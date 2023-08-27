import json
import os
from typing import Any


def read_json(file_path: str) -> dict[str, Any]:
    """Read json file"""
    if not os.path.isfile(file_path) or file_path.split(".")[-1] != "json":
        raise ValueError("No valid file was specified")

    with open(file_path) as file:
        return json.load(file)
