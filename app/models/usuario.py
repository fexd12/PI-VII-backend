from app import db
from app.auxiliar import AutoAttributes

class Usuario(db.Model,AutoAttributes):
    __tablename__ = 'usuario'
    id_usuario = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.Text, nullable = False, unique=True)
    email = db.Column(db.Text, nullable = False, unique=True)
    ativo =  db.Column(db.Text)
    endereco = db.Column(db.Text)
    cidade = db.Column(db.Text)
    uf = db.Column(db.Text)

    funcao_id = db.Column(db.Integer, db.ForeignKey('funcao.id_funcao'))

    cadastro_usuario = db.relationship('Cadastro', backref='cadastro_usuario', lazy=True)

    attrs = ['id_usuario','nome','email','ativo','funcao_id']
