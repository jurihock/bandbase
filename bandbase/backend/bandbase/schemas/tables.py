from pydantic import BaseModel
from typing import Dict, List, Optional, Union


class TableBadge(BaseModel):
    column: str
    text: Optional[str] = None
    tooltip: Optional[str] = None
    style: Optional[str] = None


class TableColumn(BaseModel):
    name: str
    filterable: bool
    sortable: bool


class TableRow(BaseModel):
    id: int
    values: Dict[str, Optional[str]]
    actions: Dict[str, str]
    badge: Optional[TableBadge] = None


class TableQuery(BaseModel):
    probe: Optional[bool] = False
    filter: Optional[Dict[str, str]] = {}
    sort: Optional[Dict[str, str]] = {}
    limit: Optional[int] = 0
    offset: Optional[int] = 0

    def get_filter_value(self, key: str):
        value = self.filter.get(key, None)
        value = [_.strip() for _ in value.split(' ') if _.strip()] \
                if value and value.strip() else None
        return value

    def get_sort_value(self, key: str):
        value = self.sort.get(key, None)
        value = value if value in ['+', '-'] else None
        return value


class Table(BaseModel):
    query: TableQuery
    columns: List[TableColumn]
    rows: List[TableRow]
    total: int
