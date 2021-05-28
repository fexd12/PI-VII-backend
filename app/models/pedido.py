from app import db
from app.auxiliar import AutoAttributes

class Pedido(db.Model,AutoAttributes):
    __tablename__ = 'pedido'

    id_pedido = db.Column(db.Integer,primary_key=True)
    cod_pedido = db.Column(db.Text,unique=True)
    data = db.Column(db.Text)

    status_id = db.Column(db.Integer, db.ForeignKey('status.id_status'))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'))

    pedidos_produto = db.relationship('ProdutosPedidos', backref='pedidos_produto', lazy=True)
    envio = db.relationship('Envio', backref='envio', lazy=True)

    attrs = ['id_funcao','descricao','cod_pedido','usuario_id','pedidos_produto','envio']