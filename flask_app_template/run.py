# -*- coding: utf-8 -*-

from gevent import monkey
from gevent.wsgi import WSGIServer
from gevent import pool
from logging import FileHandler

import gevent
import argparse
import logging
import signal
import sys
import os

from flask_app_template.common.http import CustomWSGIHandler
from flask_app_template.app import create_app


monkey.patch_all()


def argv_parse():
    parser = argparse.ArgumentParser(
        add_help=True,
        description='Flask APP Template Daemon',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-s', '--pool', type=int, default=32, help='Gevent pool size')
    parser.add_argument('-c', '--config', type=str, required=True, help='Path to config file')
    parser.add_argument('-l', '--listen', type=str, required=True, help='Listen ip')
    parser.add_argument('-p', '--port', type=int, required=True, help='Listen port')
    parser.add_argument('-L', '--access', type=str, required=True, help='Path to access log file')

    return parser.parse_args()


def main():
    global pool

    args = argv_parse()

    gevent.signal(signal.SIGQUIT, gevent.kill)

    app = create_app(args.config)

    pool = pool.Pool(args.pool)

    """ Gevent logger
    """

    handler = FileHandler(os.path.realpath(args.access))

    access_log = logging.getLogger('access')
    access_log.addHandler(handler)
    access_log.setLevel(logging.DEBUG)

    try:
        with app.app_context():
            ws = WSGIServer((args.listen, args.port), app, spawn=pool, 
                log=access_log, error_log=app.logger, 
                handler_class=CustomWSGIHandler)
            ws.serve_forever()
    except KeyboardInterrupt:
        print 'Exit...'
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    except Exception as error:
        print error


if __name__ == '__main__':
    main()
