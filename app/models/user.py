from .. import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    # Additional fields
    nome = db.Column(db.String(200), nullable=False, unique=True,
                     default='Unnamed')
    email = db.Column(db.String(200), nullable=False, unique=True)
    senha = db.Column(db.String(200), nullable=False)
    data_cadastro = db.Column(db.DateTime)
    is_admin = db.Column(db.Boolean, nullable=False)

    # Relationships
    interested_courses =\
        db.relationship('Course',
                        secondary=usuarios_cursos_interesse,
                        backref=db.backref('users_interested', lazy='dynamic'),
                        lazy='dynamic'
                        )

    def __init__(self, nome, senha, email):
        self.nome = nome
        self.senha = senha
        self.email = email
        self.data_cadastro = datetime.now()
        self.is_admin = False

    def __repr__(self):
        return 'User {}>'.format(self.id)


class UserReport(db.Model):
    __tablename__ = 'usuarios_relatorio'

    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    id_area_conhecimento = db.Column(db.Integer,
                                     db.ForeignKey('areas_conhecimento.id'))
    numero_acertos = db.Column(db.Integer)
    numero_erros = db.Column(db.Integer)

    def __init__(self):
        self.id_usuario = id_usuario
        self.id_area_conhecimento = id_area_conhecimento
        self.numero_acertos = 0
        self.numero_erros = 0


usuarios_cursos_interesse =\
    db.Table('usuarios_cursos_interesse',
             db.Column('id_usuario',
                       db.Integer,
                       db.ForeignKey('usuarios.id')
                       ),
             db.Column('id_instituicao_ensino', db.Integer,
                       db.ForeignKey('instituicoes_ensino.id')
                       ),
             db.Column('id_curso', db.Integer, db.ForeignKey('cursos.id'))
             )
