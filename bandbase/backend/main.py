import click
import uvicorn

import bandbase.defaults
import bandbase.imprint


@click.command()
@click.option('-h', '--host', type=str, default=bandbase.defaults.host, help='Bind socket to this host.')
@click.option('-p', '--port', type=int, default=bandbase.defaults.port, help='Bind socket to this port.')
@click.option('-d', '--debug', is_flag=True, default=bandbase.defaults.debug, help='Enable debug mode.')
@click.option('-c', '--config', type=str, default=bandbase.defaults.config, help='Configuration file path.')
@click.option('-l', '--logs', type=str, default=bandbase.defaults.logs, help='Log file directory.')
@click.version_option(prog_name=bandbase.imprint.name, version=bandbase.imprint.version, message='%(prog)s v%(version)s')
def main(host, port, debug, config, logs):

    bandbase.defaults.host = host
    bandbase.defaults.port = port
    bandbase.defaults.debug = debug
    bandbase.defaults.config = config
    bandbase.defaults.logs = logs

    # TODO
    # logging.getLogger('uvicorn').handlers
    # https://stackoverflow.com/a/63496366

    uvicorn.run('bandbase.app:app',
                host=host,
                port=port,
                debug=debug,
                reload=debug)


if __name__ == '__main__':

    main()
