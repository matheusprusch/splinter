from flask import jsonify, request
from flask_restful import Resource, Api, reqparse
from flask_restful import fields, marshal_with, abort, marshal

from . import api as api_bp
from .. import db
from ..models.question import Question as QuestionModel

api = Api(api_bp)

question_fields = {
    'id': fields.Integer,
    'id_concurso': fields.Integer,
    'id_area_conhecimento': fields.Integer,
    'descricao': fields.String,
    'numero_acertos': fields.Integer,
    'numero_erros': fields.Integer
}


class Question(Resource):

    @marshal_with(question_fields)
    def get(self, id):
        question = QuestionModel.query.filter_by(id=id).first_or_404()
        return question, 200


class QuestionsList(Resource):
    def get(self):
        questions = QuestionModel.query.all()
        return {'questions': marshal(questions, question_fields)}, 200

    @marshal_with(question_fields)
    def post(self):
        args = request.get_json(force=True)
        if QuestionModel.query.\
            filter(QuestionModel.descricao == args['descricao']).first():
            abort(409, message="This question already exists.")
        question = QuestionModel(args['id_concurso'],
                                       args['id_area_conhecimento'],
                                       args['descricao'])
        db.session.add(question)
        db.session.commit()
        return question, 201


class QuestionsExamination(Resource):
    def get(self, examination_id):
        questions = QuestionModel.query.filter_by(id_concurso=examination_id).all()
        return {'questions': marshal(questions, question_fields)}, 200


api.add_resource(QuestionsList, '/questions')
api.add_resource(QuestionsExamination, '/questions/examination/<int:examination_id>')
api.add_resource(Question, '/question/<int:id>')
