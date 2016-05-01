from flask import jsonify, request

from . import api
from .. import db
from ..models.institution import Institution


@api.route('/institutions', methods=['GET'])
def get_institutions():
    pass


@api.route('/institutions/<int:id>', methods=['GET'])
def get_institution(id):
    pass


@api.route('/institutions', methods=['POST'])
def create_institution():
    pass


@api.route('/institutions/<int:id>', methods=['PUT'])
def update_institution(id):
    pass


@api.route('/institutions/<int:id>', methods=['DELETE'])
def delete_institution(id):
    pass
