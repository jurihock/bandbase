import flask

from handlers.errors import *

class RequestHandler(object):

    def __init__(self, id=None):

        self.id = id

    def handle(self):

        method = flask.request.method

        if    method == 'GET':  return self.handle_get()
        elif  method == 'POST': return self.handle_post()
        else: raise MethodNotSupportedError(method)

    def handle_get(self):  raise FunctionNotSupportedError('handle_get')
    def handle_post(self): raise FunctionNotSupportedError('handle_post')

    def query(self):

        method = flask.request.method

        if    method == 'GET':  return self.query_get()
        elif  method == 'POST': return self.query_post()
        else: raise MethodNotSupportedError(method)

    def query_get(self):  raise FunctionNotSupportedError('query_get')
    def query_post(self): raise FunctionNotSupportedError('query_post')

    def add(self):

        method = flask.request.method

        if    method == 'GET':  return self.add_get()
        elif  method == 'POST': return self.add_post()
        else: raise MethodNotSupportedError(method)

    def add_get(self):  raise FunctionNotSupportedError('add_get')
    def add_post(self): raise FunctionNotSupportedError('add_post')

    def update(self):

        method = flask.request.method

        if    method == 'GET':  return self.update_get()
        elif  method == 'POST': return self.update_post()
        else: raise MethodNotSupportedError(method)

    def update_get(self):  raise FunctionNotSupportedError('update_get')
    def update_post(self): raise FunctionNotSupportedError('update_post')

    def delete(self):

        method = flask.request.method

        if    method == 'GET':  return self.delete_get()
        elif  method == 'POST': return self.delete_post()
        else: raise MethodNotSupportedError(method)

    def delete_get(self):  raise FunctionNotSupportedError('delete_get')
    def delete_post(self): raise FunctionNotSupportedError('delete_post')
