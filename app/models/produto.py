from app import db
from app.auxiliar import AutoAttributes

class Produto(db.Model,AutoAttributes):
    __tablename__ = 'produto'
    id_produto = db.Column(db.Integer,primary_key=True)

    descricao = db.Column(db.Text)

    produtos_pedidos = db.relationship('ProdutosPedidos', backref='produtos_pedidos', lazy=True)

    attrs = ['id_produto','descricao','produtos_pedidos']