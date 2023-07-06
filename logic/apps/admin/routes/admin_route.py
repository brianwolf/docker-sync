from flask import Blueprint, jsonify

from logic.apps.admin.config.variables import Vars
from logic.libs.logger.logger import get_log
from logic.libs.variables.variables import get_var

blue_print = Blueprint('admin', __name__, url_prefix='/')


@blue_print.route('/')
def alive():
    version = get_var(Vars.VERSION)
    get_log().info(f'Version: {version}')
    return jsonify(version=version)
