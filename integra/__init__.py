import os
from flask import Flask
import _thread
from integra.monitor import handler
import logging
from integra.monitor.dict import dict_helpers as dh


def create_app(test_config=None):
    if os.environ.get('FLASK_ENV') == 'production':
        app = Flask(__name__, instance_relative_config=True, instance_path='/etc/integra')
    else:
        app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    app.logger.setLevel(logging.DEBUG)

    _thread.start_new_thread(launch_server, (app, ))

    app.logger.info("Flask app initialized.")
    app.logger.debug("Flask instance path: " + app.instance_path)

    return app


def launch_server(app: Flask):
    app.logger.info('Starting integra server process')

    server = handler.IntegraTCPServer((
        app.config['LISTEN_HOST'] if 'LISTEN_HOST' in app.config else "localhost",
        int(app.config['LISTEN_PORT'] if 'LISTEN_PORT' in app.config else 7878)),
        handler.IntegraTCPHandler, app=app, slow=dh.load_slow())
    server.serve_forever()




