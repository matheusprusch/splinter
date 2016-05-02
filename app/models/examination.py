from .. import db


class Examination(db.Model):
    __tablename__ = 'concursos'

    id = db.Column(db.Integer, primary_key=True)
    # Additional fields
    id_instituicao_ensino = db.Column(db.Integer,
                                      db.ForeignKey('instituicoes_ensino.id'))
    institutions = db.relationship('Institution', backref='examinations',
                                   lazy='dynamic')
    nome = db.Column(db.String(200), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    semestre = db.Column(db.Integer)
    data_inicio = db.Column(db.DateTime)
    duracao = db.Column(db.Integer)

    def __init__(self, id_instituicao_ensino, nome, ano,
                 semestre, data_inicio, duracao):
        self.id_instituicao_ensino = id_instituicao_ensino
        self.nome = nome
        self.ano = ano
        self.semestre = semestre
        self.data_inicio = data_inicio
        self.duracao = duracao

    def __repr__(self):
        return 'Examination {}>'.format(self.id)
