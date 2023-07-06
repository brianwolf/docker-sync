from flask import Blueprint

from logic.apps.sync import service

blue_print = Blueprint('sync', __name__, url_prefix='/api/v1/sync')


@blue_print.route('/', methods=['GET'])
def sync():
    service.sync()
    return '', 200
