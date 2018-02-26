# -*- coding: utf-8 -*-

from flask import Blueprint, request, current_app, abort, jsonify
from flask_restful import Resource, Api, reqparse

from flask_app_template.models import *
from flask_app_template.common.helpers import *


class Example(Resource):

    def get(self):
        return jsonify({'message': 'ok'})


example_module = Blueprint(__name__, __name__)

api_example_module = Api(example_module)
api_example_module.add_resource(Example, '/example')
