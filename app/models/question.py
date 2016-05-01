from .. import db


class Question(db.Model):
    __tablename__ = 'questoes'

    id = db.Column(db.Integer, primary_key=True)
    # Additional fields

    def __repr__(self):
        return 'Question {}>'.format(self.id)
