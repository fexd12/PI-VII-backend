from app import db
from app.auxiliar import AutoAttributes

class Cores(db.Model,AutoAttributes):
    __tablename__ = 'cores'
    id_cores = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.Text, nullable = False, unique=True)

    attrs = ['id_cores','nome']
