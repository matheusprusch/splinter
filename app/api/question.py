from flask import jsonify, request

from . import api
from .. import db
from ..models.question import Question


@api.route('/questions', methods=['GET'])
def get_questions():
    pass


@api.route('/questions/<int:id>', methods=['GET'])
def get_question(id):
    pass


@api.route('/questions', methods=['POST'])
def create_question():
    pass


@api.route('/questions/<int:id>', methods=['PUT'])
def update_question(id):
    pass


@api.route('/questions/<int:id>', methods=['DELETE'])
def delete_question(id):
    pass
