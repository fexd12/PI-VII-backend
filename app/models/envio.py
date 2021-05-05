from app import db
from app.auxiliar import AutoAttributes

class Envio(db.Model,AutoAttributes):
    __tablename__ = 'envio'
    id_envio = db.Column(db.Integer, primary_key = True)

    codigo_envio = db.Column(db.Text)
    qr_code = db.Column(db.Text)
    token = db.Column(db.Text)

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'))

    attrs = ['id_envio','codigo_envio','qr_code','token',' usuario_id']
