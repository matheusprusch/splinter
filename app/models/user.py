from .. import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    # Additional fields
    nome = db.Column(db.String(200), nullable=False, unique=True,
                     default='Unnamed')
    email = db.Column(db.String(200), nullable=False, unique=True)
    data_cadastro = db.Column(db.DateTime)

    def __init__(self):
        self.nome = nome
        self.senha = senha
        self.email = email
        self.data_cadastro = datetime.now()

    def __repr__(self):
        return 'User {}>'.format(self.id)
