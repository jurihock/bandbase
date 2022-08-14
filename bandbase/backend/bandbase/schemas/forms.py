from pydantic import BaseModel
from typing import Dict, List, Optional


class Acknowledgment(BaseModel):
    id: int
    name: str
