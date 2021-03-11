from app import db
from app.auxiliar import AutoAttributes

class Funcao(db.Model,AutoAttributes):
    __tablename__ = 'funcao'
    id_funcao = db.Column(db.Integer,primary_key=True)
    descricao = db.Column(db.Text)

    funcao = db.relationship('Usuario', backref='funcoes', lazy=True)

    attrs = ['id_funcao','descricao']