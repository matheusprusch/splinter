from flask import jsonify, request

from . import api
from .. import db
from ..models.course import Course


@api.route('/courses', methods=['GET'])
def get_courses():
    pass


@api.route('/courses/<int:id>', methods=['GET'])
def get_course(id):
    pass


@api.route('/courses', methods=['POST'])
def create_course():
    pass


@api.route('/courses/<int:id>', methods=['PUT'])
def update_course(id):
    pass


@api.route('/courses/<int:id>', methods=['DELETE'])
def delete_course(id):
    pass
