from .. import db
from . import examination


class Institution(db.Model):
    __tablename__ = 'instituicoes_ensino'

    id = db.Column(db.Integer, primary_key=True)
    # Additional fields
    sigla = db.Column(db.String(25), unique=True)
    nome = db.Column(db.String(200), unique=True, nullable=False)
    site = db.Column(db.String(100), unique=True, nullable=False)
    privado = db.Column(db.Boolean, nullable=False)

    def __init__(self, sigla, nome, site, privado):
        self.sigla = sigla
        self.nome = nome
        self.site = site
        self.privado = privado

    def __repr__(self):
        string = {"id": self.id,
                  "sigla": self.sigla,
                  "nome": self.nome,
                  "site": self.site,
                  "privado": self.privado}
        return str(string)
