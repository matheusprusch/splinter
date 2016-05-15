# coding=utf-8
from flask import jsonify, request
from flask_restful import Resource, Api, reqparse
from flask_restful import fields, marshal_with, abort, marshal

from . import api as api_bp
from .. import db
from ..models.examination import Examination as ExaminationModel

api = Api(api_bp)

examination_fields = {
    'id': fields.Integer,
    'id_instituicao_ensino': fields.Integer,
    'nome': fields.String,
    'ano': fields.String,
    'semestre': fields.Integer,
    'data_inicio': fields.DateTime,
    'duracao': fields.Integer,
    'uri': fields.Url('api.examination', absolute=True)
}

parser = reqparse.RequestParser()
parser.add_argument('id', help="ID do concurso", required=False)
parser.add_argument('id_instituicao_ensino', help="ID da instituicao que tem o concurso", required=False)
parser.add_argument('nome', help="Nome do concurso")
parser.add_argument('ano', help="Ano do concurso")
parser.add_argument('semestre', help="Semestre do concurso")
parser.add_argument('duracao', help="Duracao do concurso")


class Examination(Resource):

    @marshal_with(examination_fields)
    def get(self, id):
        examination = ExaminationModel.query.filter_by(id=id).first_or_404()
        return examination, 200

    @marshal_with(examination_fields)
    def put(self, id):
        args = request.get_json(force=True)
        examination = ExaminationModel.query.filter_by(id=id).first_or_404()

        # Make sure required fields are there
        if args['nome'] and args['ano'] and args['semestre'] is not None:

            # Make sure the fields are unique
            if ExaminationModel.query.filter(ExaminationModel.id != args['id']).\
                filter((ExaminationModel.nome == args['nome']) |
                       (ExaminationModel.ano == args['ano']) |
                       (ExaminationModel.semestre == args['semestre'])
                       ).first():
                abort(409,
                      message="An examination with this name already exists")
            else:
                examination.id_instituicao_ensino = args['id_instituicao_ensino']
                examination.nome = args['nome']
                examination.ano = args['ano']
                examination.semestre = args['semestre']
                examination.data_inicio = args['data_inicio']
                examination.duracao = args['duracao']
        else:
            abort(409, message="Missing fields")

        # Commit and return
        db.session.commit()
        examination.id
        return examination


class ExaminationList(Resource):

    def get(self):
        examinations = ExaminationModel.query.all()
        return {'examinations': marshal(examinations, examination_fields)}, 200

    @marshal_with(examination_fields)
    def post(self):
        args = request.get_json(force=True)
        if ExaminationModel.query.\
            filter((ExaminationModel.nome == args['nome']) |
                   (ExaminationModel.ano == args['ano']) |
                   (ExaminationModel.semestre == args['semestre'])
                   ).first():
            abort(409, message="This examination already exists.")

        examination = ExaminationModel(args['id_instituicao_ensino'],
                                       args['nome'],
                                       args['ano'],
                                       args['semestre'],
                                       args['data_inicio'],
                                       args['duracao'])
        db.session.add(examination)
        db.session.commit()
        return examination, 201

api.add_resource(ExaminationList, '/examinations')
api.add_resource(Examination, '/examination/<int:id>')
