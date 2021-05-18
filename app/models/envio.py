from app import db
from app.auxiliar import AutoAttributes

class Envio(db.Model,AutoAttributes):
    __tablename__ = 'envio'
    id_envio = db.Column(db.Integer, primary_key = True)

    codigo_envio = db.Column(db.Text)
    qr_code = db.Column(db.Text)
    token = db.Column(db.Text)
    codigo_pedido = db.Column(db.Text, db.ForeignKey('pedido.cod_pedido'))

    attrs = ['id_envio','codigo_envio','qr_code','token','codigo_pedido']
