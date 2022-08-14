from pydantic import BaseModel
from typing import Dict, List, Optional


class ListItem(BaseModel):
    id: int
    name: str
    pinned: bool


class List(BaseModel):
    items: List[ListItem]
    default: Optional[int]
    nullable: bool
