from datetime import datetime
from .. import db


class Practice(db.Model):
    __tablename__ = 'praticar_questoes'

    id = db.Column(db.Integer, primary_key=True)
    # Additional fields
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    id_questao = db.Column(db.Integer, db.ForeignKey('questoes.id'))
    alternativa_usuario = db.Column(db.Integer,
                                    db.ForeignKey('questoes_alternativas.id'))
    data_hora = db.Column(db.DateTime)

    # Relationships
    question = db.relationship('Question',
                               backref=db.backref('practices', lazy='dynamic'),
                               lazy='select')
    choice = db.relationship('Alternatives',
                             backref=db.backref('practices', lazy='dynamic'),
                             lazy='select')
    user = db.relationship('User',
                           backref=db.backref('practice_questions',
                                              lazy='dynamic'),
                           lazy='select')

    def __init__(self, id_usuario, id_questao, alternativa_usuario):
        self.id_usuario = id_usuario
        self.id_questao = id_questao
        self.alternativa_usuario = alternativa_usuario
        self.data_hora = datetime.now()

    def __repr__(self):
        return 'Practice {}>'.format(self.id)
