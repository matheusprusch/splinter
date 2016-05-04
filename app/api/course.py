# coding=utf-8
from flask import jsonify, request
from flask_restful import Resource, Api, reqparse
from flask_restful import fields, marshal_with, abort, marshal

from . import api as api_bp
from .. import db
from ..models.course import Course as CourseModel
from ..models.institution import Institution as InstitutionModel

api = Api(api_bp)

institution_fields = {
    'id': fields.Integer,
    'sigla': fields.String,
    'nome': fields.String,
    'site': fields.String,
    'uri': fields.Url('api.institution', absolute=True)
}

resource_fields = {
    'id': fields.Integer,
    'nome': fields.String,
    'descricao': fields.String,
    'instituicoes': fields.Nested(institution_fields),
    'uri': fields.Url('api.course', absolute=True)
}

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('id', help="ID do curso", required=False)
parser.add_argument('nome', help="Titulo do curso")
parser.add_argument('descricao', help="Descrição do curso")
parser.add_argument('instituicoes', type=list,
                    help="Instituições que oferecem o curso", location='json')


class Course(Resource):

    @marshal_with(resource_fields)
    def get(self, id):
        c = CourseModel.query.filter_by(id=id).first_or_404()
        return c, 200

    @marshal_with(resource_fields)
    def put(self, id):
        course = CourseModel.query.filter_by(id=id).first_or_404()
        args = parser.parse_args()

        # Modify name
        if args['nome'] and args['nome'] == course.nome:
            pass
        elif args['nome'] and not CourseModel.query.\
                filter_by(nome=args['nome']).first():
            course.nome = args['nome']
        else:
            abort(409,
                  message="You must specify a unique and valid title")

        # Modify description
        course.descricao = args['descricao']

        if 'instituicoes' in args and args['instituicoes'] > 0:
            # Get the ids of institutions already linked
            existing_institutions = [instituicoes.id for
                                     instituicoes in course.instituicoes]

            for i in args['instituicoes']:
                if i in existing_institutions:
                    # We shouldn't do anything. It'd cause duplicate pk
                    continue
                else:
                    course.instituicoes.append(
                        InstitutionModel.query.filter_by(id=i).first()
                    )
        else:
            abort(400, message="A course must have a linked institution")

        # Commit and return
        db.session.commit()
        course.id
        return course


class CourseList(Resource):

    def get(self):
        courses = CourseModel.query.all()

        return {'courses': marshal(courses, resource_fields)}, 200

    @marshal_with(resource_fields)
    def post(self):
        args = parser.parse_args()
        if CourseModel.query.filter_by(nome=args['nome']).first():
            abort(409, message="A course with this name already exists.")
        course = CourseModel(args['nome'], args['descricao'])
        for i in args['instituicoes']:
            institution = InstitutionModel.query.filter_by(id=i).first()
            if institution:
                course.instituicoes.append(institution)
            else:
                abort(500, message="Unable to find institution with id "+i)
        db.session.add(course)
        db.session.commit()
        course.id
        return course, 201

api.add_resource(CourseList, '/courses')
api.add_resource(Course, '/course/<int:id>')
