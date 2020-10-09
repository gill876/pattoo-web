#!/usr/bin/env python3
"""Pattoo WSGI script.

Serves as a Gunicorn WSGI entry point for pattoo-api

"""

# Standard libraries
import sys
import os
# Try to create a working PYTHONPATH
_BIN_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
_ROOT_DIRECTORY = os.path.abspath(os.path.join(_BIN_DIRECTORY, os.pardir))
_EXPECTED = '{0}pattoo-web{0}bin'.format(os.sep)
if _BIN_DIRECTORY.endswith(_EXPECTED) is True:
    sys.path.append(_ROOT_DIRECTORY)
else:
    print('''This script is not installed in the "{0}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)

# Pattoo libraries
from pattoo_shared import log
from pattoo_shared.agent import Agent, AgentCLI, AgentAPI
from pattoo_web.constants import (
    PATTOO_WEBD_NAME, PATTOO_WEBD_PROXY)
from pattoo_web.configuration import Config
from pattoo_web.web import PATTOO_WEBD


def main():
    """Start the Gunicorn WSGI."""
    # Initialize key variables
    config = Config()

    # Get PID filenename for Gunicorn
    agent_gunicorn = Agent(PATTOO_WEBD_PROXY, config=config)

    # Get configuration
    agent_api = AgentAPI(
        PATTOO_WEBD_NAME,
        PATTOO_WEBD_PROXY,
        PATTOO_WEBD,
        config=config)

    # Do control (API first, Gunicorn second)
    cli = AgentCLI()
    cli.control(agent_api)
    cli.control(agent_gunicorn)


if __name__ == '__main__':
    log.env()
    main()
