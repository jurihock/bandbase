import sqlalchemy
import sqlalchemy.sql
import sqlalchemy.sql.functions
from typing import List


def AND(*_):        return sqlalchemy.and_(*_)
def ASC(_):         return sqlalchemy.sql.asc(_)
def CAST(_, __):    return sqlalchemy.cast(_, __)
def CONCAT(*_):     return sqlalchemy.sql.functions.concat(*_)
def DESC(_):        return sqlalchemy.sql.desc(_)
def EXTRACT(_, __): return sqlalchemy.extract(_, __)
def IGNORECASE(_):  return sqlalchemy.sql.func.lower(_)
def MAX(_):         return sqlalchemy.func.max(_)
def MIN(_):         return sqlalchemy.func.min(_)
def NOW():          return sqlalchemy.func.now()
def OR(*_):         return sqlalchemy.or_(*_)
def QUERY(_):       return sqlalchemy.text(_)
def TOCHAR(_, __):  return sqlalchemy.func.to_char(_, __)


def LIKE(sql, column, values: List[str]):
    from sqlalchemy.sql.sqltypes import String
    if type(column) in [list, tuple]:
        return sql.filter(AND(OR(subcolumn.cast(String).ilike(f'%{_}%') for subcolumn in column) for _ in values)) \
               if values else sql
    else:
        return sql.filter(AND(column.cast(String).ilike(f'%{_}%') for _ in values)) \
               if values else sql


def LIMITOFF(sql, limit: int, offset: int):
    sql = sql.limit(limit) if limit > 0 else sql
    sql = sql.offset(offset) if offset > 0 else sql
    return sql


def ORDERBY(sql, column, value: str):
    from sqlalchemy.sql.sqltypes import String
    if type(column.property.columns[0].type) is String:
        return sql.order_by(ASC(IGNORECASE(column))) \
               if value == '+' else \
               sql.order_by(DESC(IGNORECASE(column))) \
               if value == '-' else sql
    else:
        return sql.order_by(ASC(column)) \
               if value == '+' else \
               sql.order_by(DESC(column)) \
               if value == '-' else sql
