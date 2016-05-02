from flask import jsonify, request

from . import api
from .. import db
from ..models.practice import Practice


@api.route('/practices', methods=['GET'])
def get_practices():
    pass


@api.route('/practices/<int:id>', methods=['GET'])
def get_practice(id):
    pass


@api.route('/practices', methods=['POST'])
def create_practice():
    pass


@api.route('/practices/<int:id>', methods=['PUT'])
def update_practice(id):
    pass


@api.route('/practices/<int:id>', methods=['DELETE'])
def delete_practice(id):
    pass
