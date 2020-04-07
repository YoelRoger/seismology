from .. import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    admin = db.Column(db.Boolean)

    def __repr__(self):
        return '<User: %r %r >' % (self.email, self.password, self.admin)
