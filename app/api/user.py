# coding=utf-8
from flask import jsonify, request
from flask_restful import Resource, Api, reqparse
from flask_restful import fields, marshal_with, abort, marshal

from sqlalchemy.exc import IntegrityError

from . import api as api_bp
from .. import db
from ..models.user import User as UserModel, UserReport as UserReportModel

api = Api(api_bp)

user_fields = {
    'id': fields.Integer,
    'nome': fields.String,
    'email': fields.String,
    'senha': fields.String,
    'is_admin': fields.Boolean,
    'data_cadastro': fields.DateTime,
    'uri': fields.Url('api.user', absolute=True)
}

report_fields = {
    'area_conhecimento': fields.String,
    'numero_acertos': fields.Integer,
    'numero_erros': fields.Integer,
    'media': fields.Float
}

user_report_fields = {
    'nome': fields.String,
    'report': fields.Nested(report_fields),
    'uri': fields.Url('api.user', absolute=True)
}

parser = reqparse.RequestParser()
parser.add_argument('id', help="ID do usuário", required=False)
parser.add_argument('nome', help="Nome do usuário")
parser.add_argument('email', help="Email do usuário")
parser.add_argument('senha', help="Senha do usuário")
parser.add_argument('is_admin', type=bool, help='Se o usuário é administrador')
parser.add_argument('data_cadastro', help="Data de cadastro do usuário", required=False)

class User(Resource):

    @marshal_with(user_fields)
    def get(self, id):
        c = UserModel.query.filter_by(id=id).first_or_404()
        return c, 200

    @marshal_with(user_fields)
    def put(self, id):
        args = request.get_json(force=True)
        user = UserModel.query.filter_by(id=id).first_or_404()

        # Make sure required fields are there
        if args['nome'] is not None:

            # Make sure the fields are unique
            if UserModel.query.filter(UserModel.id != args['id']).\
                filter(UserModel.nome == args['email']).first():
                abort(409,
                      message="An user with this name already exists")
            else:
                user.nome = args['nome']
                user.email = args['email']
                user.senha = args['senha']
                user.is_admin = args['is_admin']
        else:
            abort(409, message="Missing fields")

        # Commit and return
        db.session.commit()
        user.id
        return user

    def delete(self, id):
        user = UserModel.query.filter_by(id=id).first_or_404()
        try:
            db.session.delete(user)
            db.session.commit()
        except IntegrityError:
            abort(409, message="You can't delete a user that is used in other models.")

        return 204


class UserList(Resource):

    def get(self):
        user = UserModel.query.all()
        return {'users': marshal(user, user_fields)}, 200

    @marshal_with(user_fields)
    def post(self):
        args = request.get_json(force=True)

        if UserModel.query.\
            filter(UserModel.nome == args['email']).first():
            abort(409, message="This user already exists.")

        user = UserModel(args['nome'],
                         args['email'],
                         args['senha'],
                         args['is_admin'])
        db.session.add(user)
        db.session.commit()
        user.id
        return user, 201

class Report(Resource):

    # @marshal_with(user_report_fields)
    def get(self):
        # user = auth.username()
        # Mestre Splinter - The master of Gambis
        user = UserModel.query.filter_by(email='splinter@example.com').first()
        if user is None:
            user = UserModel('Splinter', 'splinter@example.com', 'splinter', True)
            db.session.add(user)
            db.session.commit()

        report = UserReportModel.query.filter_by(id_usuario=user.id).all()

        report_subjects = []
        for subject in report:
            sr = SubjectReport(subject.id_area_conhecimento, subject.numero_acertos, subject.numero_erros)
            report_subjects.append(sr)

        user.report = report_subjects
        # return user, 200
        return {'reportsubjects': marshal(report_subjects, report_fields)}, 200


class SubjectReport:

    def descobre_area_conhecimento(self, id):
        from ..models.subject import Subject as SubjectModel
        subject = SubjectModel.query.filter_by(id=id).first()
        return subject.nome

    def calcula_media(self, numero_acertos, numero_erros):
        print numero_acertos, numero_erros
        print numero_erros + numero_acertos
        return round(numero_acertos / (float(numero_acertos) + float(numero_erros)),2)

    def __init__(self, id_area_conhecimento, numero_acertos, numero_erros):
        self.area_conhecimento = self.descobre_area_conhecimento(id_area_conhecimento)
        self.numero_acertos = numero_acertos
        self.numero_erros = numero_erros
        self.media = self.calcula_media(numero_acertos, numero_erros)

api.add_resource(UserList, '/users')
api.add_resource(User, '/user/<int:id>')
api.add_resource(Report, '/user/report')
