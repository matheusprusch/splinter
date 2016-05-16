from .. import db

instituicoes_ensino_curso =\
    db.Table('instituicoes_ensino_curso',
             db.Column('id_instituicao_ensino', db.Integer,
                       db.ForeignKey('instituicoes_ensino.id')),
             db.Column('id_curso', db.Integer, db.ForeignKey('cursos.id')),
             db.PrimaryKeyConstraint('id_instituicao_ensino', 'id_curso')
             )


class Course(db.Model):
    __tablename__ = 'cursos'

    id = db.Column(db.Integer, primary_key=True)
    # Additional fields
    nome = db.Column(db.String(200), unique=True, nullable=False)
    descricao = db.Column(db.Text)
    instituicoes = db.relationship('Institution',
                                   secondary=instituicoes_ensino_curso,
                                   backref=db.backref('cursos'),
                                   lazy='select')

    def __init__(self, nome, descricao):
        self.nome = nome
        self.descricao = descricao

    def __repr__(self):
        r = {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "instituicoes": self.instituicoes
            }
        return str(r)
