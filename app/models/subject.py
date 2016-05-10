from .. import db


class Subject(db.Model):
    __tablename__ = 'areas_conhecimento'

    id = db.Column(db.Integer, primary_key=True)
    # Additional fields
    nome = db.Column(db.String(200), unique=True, nullable=False)

    def __init__(self, nome):
        self.nome = nome

    def __repr__(self):
        return 'Subject {}>'.format(self.id)


class Subject_Score(db.Model):
    __tablename__ = 'areas_conhecimento_pesos'

    id = db.Column(db.Integer, primary_key=True)
    id_concurso = db.Column(db.Integer,
                            db.ForeignKey('concursos.id'))
    id_area_conhecimento = db.Column(db.Integer,
                                     db.ForeignKey('areas_conhecimento.id'))
    peso = db.Column(db.Integer, nullable=False)

    def __init__(self, id_concurso, id_area_conhecimento, peso):
        self.id_concurso = id_concurso
        self.id_area_conhecimento = id_area_conhecimento
        self.peso = peso
