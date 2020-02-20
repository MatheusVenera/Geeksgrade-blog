from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class NotaModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement='ignore_fk')
    nota = db.Column(db.Integer)
    comentario = db.Column(db.String, nullable = True)
    nome_jogo = db.Column(db.String, nullable = True)
    usuario_id = db.Column(db.String, db.ForeignKey('user_model.email'))
    #usuario = db.relationship('UserModel', back_populates='avaliacao')

    def __init__(self, nota, nome_jogo, email,comentario):
        self.nota = nota
        self.nome_jogo = nome_jogo
        self.usuario_id = email
        self.comentario = comentario
        

class UserModel(UserMixin, db.Model):
    email = db.Column(db.String(120), primary_key=True)
    nome = db.Column(db.String(64), index=True)
    data_nascimento = db.Column(db.Date, index=True)
    caminho_da_foto = db.Column(db.String, nullable = True)
    senha_hash = db.Column(db.String(128))
    #  avalicao = db.relationship('NotaModel', back_populates='usuario')

    
    def __init__(self, email, nome, data_nascimento, caminho_da_foto, senha):
        self.nome = nome
        self.email = email
        self.data_nascimento = data_nascimento
        self.caminho_da_foto = caminho_da_foto
        self.cripto_senha(senha)

    def get_id(self):
        return self.email

    def cripto_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)
