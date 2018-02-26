# -*- coding: utf-8 -*-

from flask import Flask, make_response, jsonify
from werkzeug.contrib.fixers import ProxyFix
from logging import FileHandler
from flask_migrate import Migrate
from flask_cors import CORS

import argparse
import os
import logging


""" Blueprints
"""

from flask_app_template.api.example import example_module

""" Other
"""

from flask_app_template.common.http import CustomJSONEncoder
from flask_app_template.models import db


def create_app(config):
    app = Flask(__name__)

    app.config.update(
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
        BUNDLE_ERRORS = True,
    )

    app.config.from_pyfile(os.path.realpath(config), silent=True)

    """ Logger
    """

    formatter = logging.Formatter(app.config['LOGGING_FORMAT'])

    handler = FileHandler(app.config['LOGGING_LOCATION'])
    handler.setFormatter(formatter)

    app.logger.addHandler(handler)

    app.logger.setLevel(app.config['LOGGING_LEVEL'])

    """ Config
    """

    app.json_encoder = CustomJSONEncoder

    app.wsgi_app = ProxyFix(app.wsgi_app)

    db.init_app(app)

    CORS(app)

    """ Migration
    """

    migrate = Migrate(app=app, db=db, directory=app.config['MIGRATIONS_DIRECTORY'])

    """ Blueprints
    """

    app.register_blueprint(example_module)
    
    """ Handlers
    """

    @app.errorhandler(400)
    def error_400(error):
        return make_response(jsonify({'error': str(error)}), 400)

    @app.errorhandler(401)
    def error_401(error):
        return make_response(jsonify({'error': str(error)}), 401)

    @app.errorhandler(403)
    def error_403(error):
        return make_response(jsonify({'error': str(error)}), 403)

    @app.errorhandler(404)
    def error_404(error):
        return make_response(jsonify({'error': str(error)}), 404)

    @app.errorhandler(405)
    def error_405(error):
        return make_response(jsonify({'error': str(error)}), 405)

    @app.errorhandler(500)
    def error_500(error):
        return make_response(jsonify({'error': str(error)}), 500)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    return app
