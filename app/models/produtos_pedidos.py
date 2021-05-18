from app import db
from app.auxiliar import AutoAttributes

class ProdutosPedidos(db.Model,AutoAttributes):
    __tablename__ = 'produtos_pedidos'
    id_produtos_pedidos = db.Column(db.Integer,primary_key=True)
    
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id_produto'))
    pedido_id = db.Column(db.Text, db.ForeignKey('pedido.cod_pedido'))

    attrs = ['id_produtos_pedidos','produto_id','pedido_id']
