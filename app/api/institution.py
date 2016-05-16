# coding=utf-8
from flask import jsonify, request
from flask_restful import Resource, Api, reqparse
from flask_restful import fields, marshal_with, abort, marshal

from sqlalchemy.exc import IntegrityError

from . import api as api_bp
from .. import db
from ..models.institution import Institution as InstitutionModel
from ..models.course import Course as CourseModel

api = Api(api_bp)

course_fields = {
    'id': fields.Integer,
    'nome': fields.String,
    'descricao': fields.String,
    'uri': fields.Url('api.course', absolute=True)
}

institution_fields = {
    'id': fields.Integer,
    'sigla': fields.String,
    'nome': fields.String,
    'site': fields.String,
    'privado': fields.Boolean,
    'cursos': fields.Nested(course_fields),
    'uri': fields.Url('api.institution', absolute=True)
}

parser = reqparse.RequestParser()
parser.add_argument('sigla', help='Sigla que identifica a instituição')
parser.add_argument('nome', help='Nome da instituição')
parser.add_argument('site', type=fields.inputs.url, help='URL do site da instituição')
parser.add_argument('privado', type=bool, help='Se a instituição é privada')
parser.add_argument('cursos', type=list,
                    help="Cursos oferecidos pela instituição", location='json')


class Institution(Resource):

    @marshal_with(institution_fields)
    def get(self, id):
        i = InstitutionModel.query.filter_by(id=id).first_or_404()
        return i, 200

    @marshal_with(institution_fields)
    def put(self, id):
        args = request.get_json(force=True)
        inst = InstitutionModel.query.filter_by(id=id).first_or_404()

        # Make sure required fields are there
        if args['sigla'] and args['nome'] and args['site'] and\
                args['privado'] is not None:

            # Make sure the fields are unique
            if InstitutionModel.query.filter(InstitutionModel.id != args['id']).\
                filter((InstitutionModel.sigla == args['sigla']) |
                       (InstitutionModel.nome == args['nome'])
                       ).first():
                abort(409,
                      message="An institution with this accronym or name" +
                      " already exists")
            else:
                inst.sigla = args['sigla']
                inst.nome = args['nome']
                inst.site = args['site']
                inst.privado = args['privado']

                if args['cursos']:
                    # Get the ids of cursos already linked
                    existing_institutions = [cursos.id for
                                             cursos in inst.cursos]

                    courses = []
                    for i in args['cursos']:
                        courses.append(i['id'])

                    for i in courses:
                        if i in existing_institutions:
                            # We shouldn't do anything. It'd cause duplicate pk
                             continue
                        else:
                            inst.cursos.append(
                                CourseModel.query.filter_by(id=i).first()
                            )

                    for i in existing_institutions:
                        if i in courses:
                            # We shouldn't do anything. It'd cause duplicate pk
                             continue
                        else:
                            inst.cursos.remove(
                                CourseModel.query.filter_by(id=i).first()
                            )
                else:
                    inst.cursos = []

        else:
            abort(409, message="Missing fields")

        # Commit and return
        db.session.commit()
        inst.id
        return inst

    def delete(self, id):
        institution = InstitutionModel.query.filter_by(id=id).first_or_404()
        try:
            db.session.delete(institution)
            db.session.commit()
        except IntegrityError:
            abort(409, message="You can't delete an institution that is used in other models.")

        return 204


class InstitutionsList(Resource):

    def get(self):
        institution = InstitutionModel.query.all()
        return {'institutions': marshal(institution, institution_fields)}, 200

    @marshal_with(institution_fields)
    def post(self):
        args = request.get_json(force=True)
        if InstitutionModel.query.\
            filter((InstitutionModel.sigla == args['sigla']) |
                   (InstitutionModel.nome == args['nome'])
                   ).first():
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
