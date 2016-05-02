from datetime import datetime
from .. import db


class Pretest(db.Model):
    __tablename__ = 'praticar_simulados'

    id = db.Column(db.Integer, primary_key=True)
    # Additional fields
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    data_hora_inicio = db.Column(db.DateTime, nullable=False)
    data_hora_fim = db.Column(db.DateTime)

    # Relationships
    user = db.relationship('User',
                           backref=db.backref('pretests', lazy='dynamic'),
                           lazy='select')

    def __init__(self, id_usuario):
        self.id_usuario = id_usuario
        self.data_hora_inicio = datetime.now()

    def __repr__(self):
        return 'Pretest {}>'.format(self.id)


class PretestQuestions(db.Model):
    __tablename__ = 'praticar_simulados_questoes'

    id = db.Column(db.Integer, primary_key=True)
    id_simulado = db.Column(db.Integer, db.ForeignKey('praticar_simulados.id'))
    id_questao = db.Column(db.Integer, db.ForeignKey('questoes.id'))
    alternativa_usuario = db.Column(db.Integer,
                                    db.ForeignKey('questoes_alternativas.id'))
    data_hora = db.Column(db.DateTime)

    # Relationships
    question = db.relationship('Question',
                               backref=db.backref('pretest_questions',
                                                  lazy='dynamic'),
                               lazy='select')
    choice = db.relationship('Alternatives',
                             backref=db.backref('pretest_choices',
                                                lazy='dynamic'),
                             lazy='select')

    def __init__(self, id_simulado, id_questao, id_alternativa):
        self.id_simulado = id_simulado
        self.id_questao = id_questao
        self.alternativa_usuario = id_alternativa
        self.data_hora_inicio = datetime.now()

    def __repr__(self):
        return 'PretestQuestions {}>'.format(self.id)
