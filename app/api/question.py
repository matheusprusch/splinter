from flask import jsonify, request
from flask_restful import Resource, Api, reqparse
from flask_restful import fields, marshal_with, abort, marshal

from sqlalchemy.exc import IntegrityError

from . import api as api_bp
from .. import db
from ..models.question import Question as QuestionModel, Alternatives as AlternativesModel

api = Api(api_bp)

question_fields = {
    'id': fields.Integer,
    'id_concurso': fields.Integer,
    'id_area_conhecimento': fields.Integer,
    'descricao': fields.String,
    'numero_acertos': fields.Integer,
    'numero_erros': fields.Integer
}

alternative_fields = {
    'id': fields.Integer,
    'id_questao': fields.Integer,
    'descricao': fields.String,
    'alternativa_correta': fields.Boolean,
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


class QuestionAlternativesList(Resource):
    def get(self, question_id):
        alternatives = AlternativesModel.query.filter_by(id_questao=question_id).all()
        return {'Alternatives': marshal(alternatives, alternative_fields)}, 200


class AlternativesList(Resource):

    @marshal_with(alternative_fields)
    def post(self):
        args = request.get_json(force=True)
        if AlternativesModel.query.\
            filter(AlternativesModel.descricao == args['descricao']).first():
            abort(409, message="This alternative already exists.") 
        if args['alternativa_correta'] and AlternativesModel.query.filter_by(id_questao=args['id_questao']).\
                filter(AlternativesModel.alternativa_correta == True).count() >= 1:
            abort(409, message="You can't add two correct alternatives to the same question")
        alternative = AlternativesModel(args['id_questao'],
                                       args['descricao'],
                                       args['alternativa_correta'])
        db.session.add(alternative)
        db.session.commit()
        return alternative, 201


class Alternative(Resource):
        def delete(self, id):
            alternative = AlternativesModel.query.filter_by(id=id).first_or_404()
            try:
                db.session.delete(alternative)
                db.session.commit()
            except IntegrityError:
                abort(409, message="You can't delete an alternative that is used in other models.")

            return 204

api.add_resource(QuestionsList, '/questions')
api.add_resource(QuestionsExamination, '/questions/examination/<int:examination_id>')
api.add_resource(Question, '/question/<int:id>')
api.add_resource(QuestionAlternativesList, '/question/alternatives/<int:question_id>')
api.add_resource(AlternativesList, '/alternatives')
api.add_resource(Alternative, '/alternative/<int:id>')
