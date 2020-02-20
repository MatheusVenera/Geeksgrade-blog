from flask_wtf import FlaskForm
from app.models import UserModel
from wtforms import StringField, IntegerField ,TextField, TextAreaField, SubmitField, FileField, PasswordField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, Email, EqualTo, ValidationError
from flask_uploads import UploadSet, IMAGES
from flask_wtf.file import FileAllowed, FileRequired


class CadastrarUsuarioForm(FlaskForm):
    email = StringField("E-mail", validators=[InputRequired(message="Campo obrigatório."),
                                              Email(message="Insira um endereço de e-mail válido, usando '@'.")])
    nome = StringField("Nome do usuário", validators=[InputRequired(message="Campo obrigatório.")])
    data_nascimento = DateField("Data de nascimento", validators=[InputRequired(message="Campo obrigatório.")])
    foto = FileField("Escolher foto de perfil", validators=[FileAllowed(['jpg', 'png', 'jpeg'],message='Somente imagens jpg e png!')])
    senha = PasswordField("Senha", validators=[InputRequired(message="Campo obrigatório.")])
    senha_verificadora = PasswordField("Digite novamente sua senha",validators=[InputRequired(message="Campo obrigatório"),
                                                                                EqualTo('senha')])
    submit = SubmitField("Registrar")

    def validate_email(self, email):
        email_existente= UserModel.query.filter_by(email=email.data).first()
        if email_existente:
            raise ValidationError("Email ja cadastrado")

class LogarUsuarioForm(FlaskForm):
    email = StringField("Email do usuário", validators=[InputRequired(message="Campo obrigatório."),Email(message="Insira um endereço de e-mail válido, usando '@'.")])
    senha = PasswordField("Senha", validators=[InputRequired(message="Campo obrigatório.")])
    submit = SubmitField("Logar")

class AtualizarUsuarioForm(FlaskForm):
    nome = StringField("Nome do usuário", validators=[InputRequired(message="Campo obrigatório.")])
    data_nascimento = DateField("Data de nascimento", validators=[InputRequired(message="Campo obrigatório.")])
    foto = FileField("Escolher foto de perfil", validators=[FileAllowed(['jpg', 'png', 'jpeg'],message='Somente imagens jpg e png!')])
    senha = PasswordField("Senha", validators=[InputRequired(message="Campo obrigatório.")])
    senha_verificadora = PasswordField("Digite novamente sua senha",validators=[InputRequired(message="Campo obrigatório"),
                                                                                EqualTo('senha')])
    submit = SubmitField("Salvar alteraçao")

class CadastrarNotaForm(FlaskForm):
    nota = SelectField("Nota", choices=[(None, 'Selecionar'),('1',1),('2',2),('3',3),('4',4),('5',5),('6',6),('7',7),('8',8),('9',9),('10',10)])
    comentario = TextAreaField("Comentário")
    submit = SubmitField("Postar")

class AlterarNotaForm(FlaskForm):
    nota = SelectField("Nota", choices=[(None, 'Selecionar'),('1',1),('2',2),('3',3),('4',4),('5',5),('6',6),('7',7),('8',8),('9',9),('10',10)])
    comentario = TextAreaField("Comentário")
    submit = SubmitField("Postar")
