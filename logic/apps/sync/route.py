from flask import Blueprint, request
from flask.json import jsonify

from logic.apps.sync import service
from logic.libs.exception.exception import AppException

blue_print = Blueprint('sync', __name__, url_prefix='/api/v1/sync')


@blue_print.route('/', methods=['GET'])
def sync():
    service.sync()
    return '', 200
