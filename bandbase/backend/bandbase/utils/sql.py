import sqlalchemy.sql
import sqlalchemy.sql.functions

def QUERY(_):        return sqlalchemy.text(_)

def ASC(_):          return sqlalchemy.sql.asc(_)
def DESC(_):         return sqlalchemy.sql.desc(_)

def AND(*_):         return sqlalchemy.and_(*_)
def OR(*_):          return sqlalchemy.or_(*_)

def NOW():           return sqlalchemy.func.now()
def IGNORECASE(_):   return sqlalchemy.sql.func.lower(_)
def CONCAT(*_):      return sqlalchemy.sql.functions.concat(*_)
def EXTRACT(_):      return sqlalchemy.extract(_)
def CAST(*_):        return sqlalchemy.cast(*_)
def TOCHAR(_):       return sqlalchemy.func.to_char(_)
