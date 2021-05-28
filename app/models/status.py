from app import db
from app.auxiliar import AutoAttributes

class Status(db.Model,AutoAttributes):
    __tablename__ = 'status'

    id_status = db.Column(db.Integer,primary_key=True)
    nome = db.Column(db.Text,unique=True)
    
    status_pedidos = db.relationship('Pedido', backref='status_pedidos', lazy=True)

