from flask import jsonify, request

from . import api
from .. import db
from ..models.examination import Examination


@api.route('/examinations', methods=['GET'])
def get_examinations():
    return "Hello World"


@api.route('/examinations/<int:id>', methods=['GET'])
def get_examination(id):
    pass


@api.route('/examinations', methods=['POST'])
def create_examination():
    pass


@api.route('/examinations/<int:id>', methods=['PUT'])
def update_examination(id):
    pass


@api.route('/examinations/<int:id>', methods=['DELETE'])
def delete_examination(id):
    pass
