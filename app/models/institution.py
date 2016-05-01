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
    examinations = db.relationship('Examination', backref='institution',
                                   lazy='dynamic')

    def __repr__(self):
        return 'Institution {}>'.format(self.id)
