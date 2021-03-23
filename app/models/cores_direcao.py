from app import db
from app.auxiliar import AutoAttributes

class CoresDirecao(db.Model,AutoAttributes):
    __tablename__ = 'cores_direcao'
    id_cores_direcao = db.Column(db.Integer,primary_key=True)
    
    cor_id = db.Column(db.Integer, db.ForeignKey('cores.id_cores'))
    direcao_id = db.Column(db.Integer, db.ForeignKey('direcao.id_direcao'))

    attrs = ['id_cores_direcao','cor_id','direcao_id']
