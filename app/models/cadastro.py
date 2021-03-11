from app import db
from app.authenticate import generate_hash,check_passwd
from app.auxiliar import AutoAttributes

class Cadastro(db.Model,AutoAttributes):
    __tablename__ = 'cadastro_usuario'
    id_cadastro = db.Column(db.Integer,primary_key = True)
    senha = db.Column(db.Text, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'),nullable=False,unique=True)

    def passwd(self,passwd):
        self.senha = generate_hash(passwd)
    
    def check(self,passwd):
        return check_passwd(passwd,self.senha)

    attrs = ['id_cadastro','usuario_id','senha']