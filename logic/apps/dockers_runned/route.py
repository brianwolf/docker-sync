from flask import Blueprint
from flask.json import jsonify

from logic.apps.dockers_runned import service

blue_print = Blueprint('dockers', __name__, url_prefix='/api/v1/dockers')


@blue_print.route('/', methods=['GET'])
def get():
    return jsonify(service.get_list()), 200


@blue_print.route('/<name>', methods=['DELETE'])
def delete(name: str):
    service.delete(name)
    return jsonify(service.get_list()), 200
