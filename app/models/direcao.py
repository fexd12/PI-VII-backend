from app import db
from app.auxiliar import AutoAttributes

class Direcao(db.Model,AutoAttributes):
    __tablename__ = 'direcao'
    id_direcao = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.Text, nullable = False, unique=True)

    direcao_cores = db.relationship('CoresDirecao', backref='direcao_cores', lazy=True)

    attrs = ['id_direcao','nome','direcao_cores']
