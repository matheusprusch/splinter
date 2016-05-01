from .. import db


class Examination(db.Model):
    __tablename__ = 'concursos'

    id = db.Column(db.Integer, primary_key=True)
    # Additional fields
    id_instituicao_ensino = db.Column(db.Integer,
                                      db.ForeignKey('instituicoes_ensino.id'))
    nome = db.Column(db.String(200), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    semestre = db.Column(db.Integer)
    data_inicio = db.Column(db.DateTime)

    def __repr__(self):
        return 'Examination {}>'.format(self.id)
