#!/usr/bin/env python3

# Wrapper over Uvicorn, to grab uvicorn logging level

import multiprocessing
from typing import Dict, Union

import click
import uvicorn
import gunicorn.app.base

from click_help_colors import HelpColorsCommand
from gunicorn.app.base import Application

from .conf import settings
from .conf.logging import configure_logbook

LOG_LEVELS = {
    1: 'info',
    2: 'debug',
}


def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


@click.command(cls=HelpColorsCommand, help_options_color='yellow')  # type: ignore
@click.option('-p', '--port', default=8001)
@click.option('--host', default='127.0.0.1')
@click.option('--interface', default='wsgi')
@click.option('--reload', is_flag=True)
@click.option('-v', '--verbose', count=True, help='Show more log to debug (verbose mode).')

def main(port: int, host: str, interface: str, reload: bool, verbose: int):
    # TODO: "reload" will make our logging config lost, because
    # then Uvicorn will create another process to do actual web server job.
    options: Dict[str, Union[bool, str, int]] = {
        'reload': reload,
        'port': port,
        'host': host,
        'interface': interface
    }
    configure_logbook(verbose)
    # Configure log level for uvicorn
    if verbose:
        lv = min(verbose, len(LOG_LEVELS.keys()))
        options['log_level'] = LOG_LEVELS[lv]
    else:
        options['log_level'] = 'warning'
    uvicorn.run('src.app:app', **options)


if __name__ == '__main__':
    main()
