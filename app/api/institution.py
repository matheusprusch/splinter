# coding=utf-8
from flask import jsonify, request
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort, marshal

from . import api as api_bp
from .. import db
from ..models.institution import Institution as InstitutionModel

api = Api(api_bp)

institution_fields = {
    'id': fields.Integer,
    'sigla': fields.String,
    'nome': fields.String,
    'site': fields.String,
    'uri': fields.Url('api.institution', absolute=True)
}

parser = reqparse.RequestParser()
parser.add_argument('sigla', help='Sigla que identifica a instituição')
parser.add_argument('nome', help='Nome da instituição')
parser.add_argument('site', type=fields.inputs.url,
                    help='URL do site da instituição')
parser.add_argument('privado', type=bool,
                    help='Se a instituição é privada')


class Institution(Resource):

    @marshal_with(institution_fields)
    def get(self, id):
        i = InstitutionModel.query.filter_by(id=id).first_or_404()
        return i, 200

    def put(self, institution_id):
        pass


class InstitutionsList(Resource):

    def get(self):
        ins = InstitutionModel.query.all()
        return {'institutions': marshal(ins, institution_fields)}, 200

    @marshal_with(institution_fields)
    def post(self):
        args = parser.parse_args()
        if InstitutionModel.query.filter_by(sigla=args['sigla']).first() or\
                InstitutionModel.query.filter_by(nome=args['nome']).first():
            abort(409, message="This institution already exists.")
        institution = InstitutionModel(args['sigla'],
                                       args['nome'],
                                       args['site'],
                                       args['privado'])
        db.session.add(institution)
        db.session.commit()
        return institution, 201

api.add_resource(InstitutionsList, '/institutions')
api.add_resource(Institution, '/institution/<int:id>')
