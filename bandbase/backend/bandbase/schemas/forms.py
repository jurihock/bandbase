from pydantic import BaseModel
from typing import Dict, List, Optional, Union


class Acknowledgment(BaseModel):
    id: int
    name: str
