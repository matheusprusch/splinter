# coding=utf-8
from flask import jsonify, request
from flask_restful import Resource, Api, reqparse
from flask_restful import fields, marshal_with, abort, marshal

from . import api as api_bp
from .. import db
from ..models.institution import Institution as InstitutionModel

api = Api(api_bp)

institution_fields = {
    'id': fields.Integer,
    'sigla': fields.String,
    'nome': fields.String,
    'site': fields.String,
    'privado': fields.Boolean,
    'uri': fields.Url('api.institution', absolute=True)
}

parser = reqparse.RequestParser()
parser.add_argument('sigla', help='Sigla que identifica a instituição', location='json')
parser.add_argument('nome', help='Nome da instituição', location='json')
parser.add_argument('site', type=fields.inputs.url,
                    help='URL do site da instituição', location='json')
parser.add_argument('privado', type=bool,
                    help='Se a instituição é privada', location='json')


class Institution(Resource):

    @marshal_with(institution_fields)
    def get(self, id):
        i = InstitutionModel.query.filter_by(id=id).first_or_404()
        return i, 200

    @marshal_with(institution_fields)
    def put(self, id):
        args = parser.parse_args()
        inst = InstitutionModel.query.filter_by(id=id).first_or_404()

        # Make sure required fields are there
        if args['sigla'] and args['nome'] and args['site'] and\
                args['privado'] is not None:

            # Make sure the fields are unique
            if InstitutionModel.query.filter(InstitutionModel.id != 2).\
                filter((InstitutionModel.sigla == args['sigla']) |
                       (InstitutionModel.nome == args['nome']) |
                       (InstitutionModel.site == args['site'])
                       ).first():
                abort(409,
                      message="An institution with this name, site or " +
                      "accronym already exists")
            else:
                inst.sigla = args['sigla']
                inst.nome = args['nome']
                inst.site = args['site']
                inst.privado = args['privado']
        else:
            abort(409, message="Missing fields")
        db.session.commit()
        inst.id
        return inst


class InstitutionsList(Resource):

    def get(self):
        ins = InstitutionModel.query.all()
        return {'institutions': marshal(ins, institution_fields)}, 200

    @marshal_with(institution_fields)
    def post(self):
        json_data = request.get_json(force=True)
        if InstitutionModel.query.\
            filter((InstitutionModel.sigla == json_data['sigla']) |
                   (InstitutionModel.nome == json_data['nome']) |
                   (InstitutionModel.site == json_data['site'])
                   ).first():
            abort(409, message="This institution already exists.")
        institution = InstitutionModel(json_data['sigla'],
                                       json_data['nome'],
                                       json_data['site'],
                                       json_data['privado'])
        db.session.add(institution)
        db.session.commit()
        return institution, 201

api.add_resource(InstitutionsList, '/institutions')
api.add_resource(Institution, '/institution/<int:id>')
