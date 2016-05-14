# coding=utf-8
from flask import jsonify, request
from flask_restful import Resource, Api, reqparse
from flask_restful import fields, marshal_with, abort, marshal

from . import api as api_bp
from .. import db
from ..models.course import Course as CourseModel

api = Api(api_bp)

course_fields = {
    'id': fields.Integer,
    'nome': fields.String,
    'descricao': fields.String,
    'uri': fields.Url('api.course', absolute=True)
}

parser = reqparse.RequestParser()
parser.add_argument('id', help="ID do curso", required=False)
parser.add_argument('nome', help="Titulo do curso")
parser.add_argument('descricao', help="Descrição do curso")

class Course(Resource):

    @marshal_with(course_fields)
    def get(self, id):
        c = CourseModel.query.filter_by(id=id).first_or_404()
        return c, 200

    @marshal_with(course_fields)
    def put(self, id):
        args = request.get_json(force=True)
        course = CourseModel.query.filter_by(id=id).first_or_404()

        # Make sure required fields are there
        if args['nome'] and args['descricao'] is not None:

            # Make sure the fields are unique
            if CourseModel.query.filter(CourseModel.id != args['id']).\
                filter(CourseModel.nome == args['nome']).first():
                abort(409,
                      message="An course with this name already exists")
            else:
                course.nome = args['nome']
                course.descricao = args['descricao']
        else:
            abort(409, message="Missing fields")

        # Commit and return
        db.session.commit()
        course.id
        return course

    def delete(self, id):
        course = CourseModel.query.filter_by(id=id).first_or_404()
        try:
            db.session.delete(course)
            db.session.commit()
        except IntegrityError:
            abort(409, message="You can't delete a course that is used in other models.")

        return 204


class CourseList(Resource):

    def get(self):
        course = CourseModel.query.all()
        return {'courses': marshal(course, course_fields)}, 200

    @marshal_with(course_fields)
    def post(self):
        args = request.get_json(force=True)

        if CourseModel.query.\
            filter(CourseModel.nome == args['nome']).first():
            abort(409, message="This course already exists.")

        course = CourseModel(args['nome'], args['descricao'])
        db.session.add(course)
        db.session.commit()
        course.id
        return course, 201

api.add_resource(CourseList, '/courses')
api.add_resource(Course, '/course/<int:id>')
