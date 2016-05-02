from flask import jsonify, request

from . import api
from .. import db
from ..models.pretest import Pretest


@api.route('/pretests', methods=['GET'])
def get_pretests():
    pass


@api.route('/pretests/<int:id>', methods=['GET'])
def get_pretest(id):
    pass


@api.route('/pretests', methods=['POST'])
def create_pretest():
    pass


@api.route('/pretests/<int:id>', methods=['PUT'])
def update_pretest(id):
    pass


@api.route('/pretests/<int:id>', methods=['DELETE'])
def delete_pretest(id):
    pass
