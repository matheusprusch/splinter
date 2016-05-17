# coding=utf-8
from flask import jsonify, request
from flask_restful import Resource, Api, reqparse
from flask_restful import fields, marshal_with, abort, marshal

from sqlalchemy.exc import IntegrityError

from . import api as api_bp
from .. import db
from ..models.subject import Subject as SubjectModel

api = Api(api_bp)

subject_fields = {
    'id': fields.Integer,
    'nome': fields.String,
    'uri': fields.Url('api.subject', absolute=True)
}

parser = reqparse.RequestParser()
parser.add_argument('id', help="ID do curso", required=False)
parser.add_argument('nome', help="Titulo do curso")


class Subject(Resource):

    @marshal_with(subject_fields)
    def get(self, id):
        c = SubjectModel.query.filter_by(id=id).first_or_404()
        return c, 200

    @marshal_with(subject_fields)
    def put(self, id):
        args = request.get_json(force=True)
        subject = SubjectModel.query.filter_by(id=id).first_or_404()

        # Make sure required fields are there
        if args['nome'] is not None:

            # Make sure the fields are unique
            if SubjectModel.query.filter(SubjectModel.id != args['id']).\
                filter(SubjectModel.nome == args['nome']).first():
                abort(409,
                      message="An subject with this name already exists")
            else:
                subject.nome = args['nome']
        else:
            abort(409, message="Missing fields")

        # Commit and return
        db.session.commit()
        subject.id
        return subject

    def delete(self, id):
        subject = SubjectModel.query.filter_by(id=id).first_or_404()
        try:
            db.session.delete(subject)
            db.session.commit()
        except IntegrityError:
            abort(409, message="You can't delete a subject that is used in other models.")

        return 204


class SubjectList(Resource):

    def get(self):
        subject = SubjectModel.query.all()
        return {'subjects': marshal(subject, subject_fields)}, 200

    @marshal_with(subject_fields)
    def post(self):
        args = request.get_json(force=True)

        if SubjectModel.query.\
            filter(SubjectModel.nome == args['nome']).first():
            abort(409, message="This subject already exists.")

        subject = SubjectModel(args['nome'])
        db.session.add(subject)
        db.session.commit()
        subject.id
        return subject, 201

api.add_resource(SubjectList, '/subjects')
api.add_resource(Subject, '/subject/<int:id>')
