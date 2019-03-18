import utils.request as request

from enum import Enum

class SortOrder(Enum):

    asc = 0,
    desc = 1

class RequestParser(object):

    def __init__(self, db=None):

        self.db = db

    def has(self, *args, **kwargs):   return request.has(*args, **kwargs)
    def str(self, *args, **kwargs):   return request.str(*args, **kwargs)
    def bool(self, *args, **kwargs):  return request.bool(*args, **kwargs)
    def int(self, *args, **kwargs):   return request.int(*args, **kwargs)
    def float(self, *args, **kwargs): return request.float(*args, **kwargs)
    def date(self, *args, **kwargs):  return request.date(*args, **kwargs)
    def time(self, *args, **kwargs):  return request.time(*args, **kwargs)
    def list(self, *args, **kwargs):  return request.list(*args, **kwargs)
    def enum(self, *args, **kwargs):  return request.enum(*args, **kwargs)
