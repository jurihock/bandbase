import sqlalchemy
import sqlalchemy.sql
import sqlalchemy.sql.functions

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
