import click

from fastapi import FastAPI, Request
from fastapi.exception_handlers import http_exception_handler
from fastapi.middleware.cors import CORSMiddleware

import bandbase.defaults
import bandbase.imprint
import bandbase.routers
import bandbase.core.session


class App(FastAPI):

    def __init__(self):

        click.secho('Bootstrapping the application instance {}'.format('[DEBUG]' if bandbase.defaults.debug else ''))

        super().__init__(title=bandbase.imprint.name,
                         version=bandbase.imprint.version,
                         docs_url='/docs' if bandbase.defaults.debug else None,
                         redoc_url='/redoc' if bandbase.defaults.debug else None,
                         debug=bandbase.defaults.debug)

        self.include_router(bandbase.routers.common)
        self.include_router(bandbase.routers.list)
        self.include_router(bandbase.routers.session)
        self.include_router(bandbase.routers.table)

        # seel also
        # https://fastapi.tiangolo.com/tutorial/cors
        # http://www.pierre-beitz.eu/2017/01/24/Dealing-with-CORS-in-a-Development-Environment-Using-a-Reverse-Proxy.html

        origins = \
        [
            'http://localhost:8000',
            'http://localhost:8080',
        ]

        self.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'])


app = App()


@app.on_event('startup')
def on_startup_event():

    print('STARTUP')

    bandbase.core.common.logger().info('test info')
    bandbase.core.common.logger().warning('test warning')
    bandbase.core.common.logger().error('test error')
    bandbase.core.common.logger().critical('test critical')


@app.on_event('shutdown')
def on_shutdown_event():

    print('SHUTDOWN')


@app.exception_handler(bandbase.core.session.SessionException)
async def on_session_exception(request: Request, exception: bandbase.core.session.SessionException):
    print(f'Deleting cookie "{exception.cookie}" due to session exception {exception.status_code}!')
    response = await http_exception_handler(request, exception)
    response.delete_cookie(exception.cookie)
    return response
