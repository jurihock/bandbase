import click

from fastapi import FastAPI, Request
from fastapi.exception_handlers import http_exception_handler
from fastapi.middleware.cors import CORSMiddleware

import bandbase.defaults
import bandbase.imprint
import bandbase.routers

import bandbase.core.database
import bandbase.core.session


class App(FastAPI):

    def __init__(self):

        click.secho(f'Init bandbase {"[DEBUG]" if bandbase.defaults.debug else ""}')

        super().__init__(title=bandbase.imprint.name,
                         version=bandbase.imprint.version,
                         debug=bandbase.defaults.debug,
                         docs_url='/docs' if bandbase.defaults.debug else None,
                         redoc_url='/redoc' if bandbase.defaults.debug else None)

        self.include_router(bandbase.routers.common)
        self.include_router(bandbase.routers.files)
        self.include_router(bandbase.routers.forms)
        self.include_router(bandbase.routers.lists)
        self.include_router(bandbase.routers.session)
        self.include_router(bandbase.routers.tables)

        # seel also
        # https://fastapi.tiangolo.com/tutorial/cors
        # http://www.pierre-beitz.eu/2017/01/24/Dealing-with-CORS-in-a-Development-Environment-Using-a-Reverse-Proxy.html

        origins = \
        [
            'http://localhost:8000',
            'http://localhost:8080',
        ]

        # additionally to the safelisted response headers
        # like Content-Length and Content-Type
        headers = ['Content-Disposition']

        self.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
            expose_headers=headers)


app = App()


@app.on_event('startup')
def on_startup_event():

    click.secho('STARTUP')

    bandbase.core.common.logger().info('test info')
    bandbase.core.common.logger().warning('test warning')
    bandbase.core.common.logger().error('test error')
    bandbase.core.common.logger().critical('test critical')

    bandbase.core.database.bootstrap()


@app.on_event('shutdown')
def on_shutdown_event():

    click.secho('SHUTDOWN')


@app.exception_handler(bandbase.core.session.SessionException)
async def on_session_exception(request: Request, exception: bandbase.core.session.SessionException):

    click.secho(f'Deleting cookie "{exception.cookie}" due to session exception {exception.status_code}!')

    response = await http_exception_handler(request, exception)
    response.delete_cookie(exception.cookie)

    return response
