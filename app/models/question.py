from .. import db


class Question(db.Model):
    __tablename__ = 'questoes'

    id = db.Column(db.Integer, primary_key=True)
    # Additional fields
    id_concurso = db.Column(db.Integer,
                            db.ForeignKey('concursos.id'))
    id_area_conhecimento = db.Column(db.Integer,
                                     db.ForeignKey('areas_conhecimento.id'))
    descricao = db.Column(db.Text, nullable=False, server_default='')
    numero_acertos = db.Column(db.Integer, default=0)
    numero_erros = db.Column(db.Integer, default=0)

    # Relationships
    concurso = db.relationship('Examination',
                               backref=db.backref('questoes'),
                               lazy='select')
    area_conhecimento = db.relationship('Subject',
                              backref=db.backref('questoes'),
                              lazy='select')

    def __init__(self, id_concurso, id_area_conhecimento, descricao):
        self.id_concurso = id_concurso
        self.id_area_conhecimento = id_area_conhecimento
        self.descricao = descricao
        self.numero_acertos = 0
        self.numero_erros = 0

    def __repr__(self):
        return 'Question {}>'.format(self.id)


class Alternatives(db.Model):
    __tablename__ = 'questoes_alternativas'

    id = db.Column(db.Integer, primary_key=True)
    id_questao = db.Column(db.Integer, db.ForeignKey('questoes.id'))
    descricao = db.Column(db.Text, nullable=False)
    alternativa_correta = db.Column(db.Boolean, default=False)

    # Relationships
    question = db.relationship('Question',
                               backref=db.backref('choices', lazy='dynamic'),
                               lazy='select')

    def __init__(self, id_questao, descricao, alternativa_correta):
        self.id_questao = id_questao
        self.descricao = descricao
        self.alternativa_correta = alternativa_correta


class QuestionImages(db.Model):
    __tablename__ = 'questoes_imagens'

    id = db.Column(db.Integer, primary_key=True)
    id_questao = db.Column(db.Integer, db.ForeignKey('questoes.id'))
    id_questao_alternativas =\
        db.Column(db.Integer, db.ForeignKey('questoes_alternativas.id'))
    descricao = db.Column(db.Text)
    imagem = db.Column(db.Text, nullable=False)

    # Relationships
    questions = db.relationship('Question',
                                backref=db.backref('image', lazy='select'))

    def __init__(self, id_questao, id_questao_alternativas, descricao, imagem):
        self.id_questao = id_questao
        self.id_questao_alternativas = id_questao_alternativas
        self.descricao = descricao
        self.imagem = imagem
