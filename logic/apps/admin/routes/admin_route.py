import ntpath
import os
from io import BytesIO

from flask import Blueprint, jsonify, send_file

from logic.apps.admin.config.variables import Vars
from logic.libs.logger.logger import logger
from logic.libs.variables.variables import get_var

blue_print = Blueprint('admin', __name__, url_prefix='/')


@blue_print.route('/')
def alive():
    version = get_var(Vars.VERSION)
    logger.info(f'Version: {version}')
    return jsonify(version=version)
