from flask import jsonify, request

from . import api
from .. import db
from ..models.subject import Subject


@api.route('/subjects', methods=['GET'])
def get_subjects():
    pass


@api.route('/subjects/<int:id>', methods=['GET'])
def get_subject(id):
    pass


@api.route('/subjects', methods=['POST'])
def create_subject():
    pass


@api.route('/subjects/<int:id>', methods=['PUT'])
def update_subject(id):
    pass


@api.route('/subjects/<int:id>', methods=['DELETE'])
def delete_subject(id):
    pass
