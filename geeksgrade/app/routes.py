from app import app, login
from flask import render_template, redirect, url_for
from app.forms import CadastrarNotaForm, CadastrarUsuarioForm, LogarUsuarioForm, AtualizarUsuarioForm, AlterarNotaForm
from app import db, login
from app.models import NotaModel, UserModel
from flask_login import logout_user, login_user, current_user
from app import config
from werkzeug.security import generate_password_hash, check_password_hash
import os

@app.route("/")
@app.route("/index",methods=['post','get'])
def executar_index():
    return render_template("index.html",title="Index")

@app.route("/cadastro", methods=['get', 'post'])
def cadastrar_usuario():
    form = CadastrarUsuarioForm()
    if form.validate_on_submit():
        if form.foto.data:
            nome_da_foto = Nome_foto(form.foto.data.filename,form.email.data)
            form.foto.data.save(os.path.join(app.config['UPLOAD_FOLDER'],nome_da_foto))
            usuario_cadastrado = UserModel(form.email.data,form.nome.data,form.data_nascimento.data,"images/" + nome_da_foto,form.senha.data)
        else:
            usuario_cadastrado = UserModel(form.email.data,form.nome.data,form.data_nascimento.data,"images/default.png",form.senha.data)
        db.session.add(usuario_cadastrado)
        db.session.commit()
        login_user(usuario_cadastrado)
        return redirect("/index")
    return render_template('cadastro_usuario.html', form=form)

@app.route("/remover_usuario",methods=['post','get'])
def remover_usuario():
    if not current_user.is_authenticated:
        return redirect("/logar")
    elif current_user.is_authenticated:
        notas = NotaModel.query.filter_by(usuario_id=current_user.email)
        total_de_comentarios = 0
        for i in notas:
            total_de_comentarios += 1
        for i in range(total_de_comentarios):
            db.session.delete(notas[0])
        db.session.delete(current_user)
        db.session.commit()
        return redirect("/index")

@app.route('/logar', methods=['get', 'post'])
def logar_usuario():
    form = LogarUsuarioForm()
    senha_incorreta = False
    if form.validate_on_submit():
        usuario = UserModel.query.filter_by(email=form.email.data).first()
        if usuario is not None:
            if usuario.verificar_senha(form.senha.data):
                login_user(usuario)
                return redirect("/index")
            else:
                senha_incorreta = True
    
    return render_template("logar.html", form=form, senha_incorreta=senha_incorreta)

@app.route('/logout',methods=['get','post'])
def deslogar():
    if not current_user.is_authenticated:
        return redirect("/logar")
    elif current_user.is_authenticated:
        logout_user()
        return redirect("/index")

@app.route('/perfil', methods=['get','post'])
def ver_perfil():
    if not current_user.is_authenticated:
        return redirect("/logar")
    elif current_user.is_authenticated:
        return render_template("perfil.html")

def Nome_foto(nome_arquivo,email):
    extensao = nome_arquivo.split(".")
    extensao = "." + extensao[-1]
    nome_da_foto = email + extensao
    nome_da_foto = nome_da_foto.replace("@", "_arroba_")
    return nome_da_foto

@app.route("/editar_perfil",methods=['post','get'])
def editar_perfil():
    if not current_user.is_authenticated:
        return redirect("/logar")
    elif current_user.is_authenticated:
        form = AtualizarUsuarioForm()
        if form.validate_on_submit():
            usuario = UserModel.query.filter_by(email = current_user.email).first()
            usuario.nome = form.nome.data
            usuario.data_nascimento = form.data_nascimento.data
            
            if type(form.foto.data) != type(""):
                nome_da_foto = Nome_foto(form.foto.data.filename,current_user.email)
                nome_da_foto = nome_da_foto.replace(".jpeg","")
                nome_da_foto = nome_da_foto.replace(".jpg","") 
                nome_da_foto = nome_da_foto.replace(".png","")
                path = app.config['UPLOAD_FOLDER']
                files = []
                # r = root , d = diretorios, f = files
                for r, d , f in os.walk(path):
                    for file in f:
                        if nome_da_foto in file:
                            files.append(os.path.join(r, file))
                for f in files:
                    for i in range(len(files)):
                        os.remove(files[i])
                nome_da_foto = Nome_foto(form.foto.data.filename, current_user.email)
                form.foto.data.save(os.path.join(app.config['UPLOAD_FOLDER'],nome_da_foto))
                usuario.caminho_da_foto = "images/" + nome_da_foto
            elif type(form.foto.data) == type(""):
                nome_da_foto = "default.png"
                usuario.caminho_da_foto = "images/" + nome_da_foto
            usuario.senha_hash= generate_password_hash(form.senha.data)    
            db.session.merge(usuario)
            db.session.commit()
            return redirect("/perfil")
        return render_template("editar_perfil.html",form=form)

@app.route("/GTA_San_Andreas",methods=['get', 'post'])
def GTA_San_andreas():
    if not current_user.is_authenticated:
        return redirect("/logar")
    elif current_user.is_authenticated:
        coments = NotaModel.query.filter_by(nome_jogo="GTA_San_Andreas")
        todos_comentarios=[]
        todas_notas=[]
        todos_usuarios = []
        lista_imagens = []
        todos_nomes = []
        for i in coments:
            todos_comentarios.append(i.comentario)
            todas_notas.append(i.nota)
            todos_usuarios.append(i.usuario_id)
        for j in todos_usuarios:        
            usuarios = UserModel.query.filter_by(email=j).first()
            lista_imagens.append(usuarios.caminho_da_foto)
            todos_nomes.append(usuarios.nome)
        if len(todas_notas) != 0:
            numero_de_usuario=len(todas_notas)
            media= sum(todas_notas)/numero_de_usuario
        else:
            numero_de_usuario= 0
            media = 0

        nota_usuario = NotaModel.query.filter_by(usuario_id=current_user.email,nome_jogo="GTA_San_Andreas").first()
        form = CadastrarNotaForm()
        form2 = AlterarNotaForm()
        if form.validate_on_submit():
            if nota_usuario is None:
                db.session.add(NotaModel(form.nota.data,"GTA_San_Andreas",current_user.email,form.comentario.data))
                db.session.commit()
                return redirect("/GTA_San_Andreas")
                
        if form2.validate_on_submit():
                nota_usuario.nota = form2.nota.data 
                nota_usuario.comentario = form2.comentario.data
                db.session.merge(nota_usuario)
                db.session.commit()
                return redirect("/GTA_San_Andreas") 
        return(render_template("GTA_San_Andreas.html", form=form,form2 = form2, nota_usuario=nota_usuario, media=media, todos_comentarios=todos_comentarios, lista_imagens=lista_imagens, todos_nomes=todos_nomes,numero_de_usuario=numero_de_usuario))

@app.route("/God_Of_War",methods=['get', 'post'])
def God_Of_War():
    if not current_user.is_authenticated:
        return redirect("/logar")
    elif current_user.is_authenticated:
        coments = NotaModel.query.filter_by(nome_jogo="God_Of_War")
        todos_comentarios=[]
        todas_notas=[]
        todos_usuarios = []
        lista_imagens = []
        todos_nomes = []
        for i in coments:
            todos_comentarios.append(i.comentario)
            todas_notas.append(i.nota)
            todos_usuarios.append(i.usuario_id)
        for j in todos_usuarios:        
            usuarios = UserModel.query.filter_by(email=j).first()
            lista_imagens.append(usuarios.caminho_da_foto)
            todos_nomes.append(usuarios.nome)
        if len(todas_notas) != 0:
            numero_de_usuario=len(todas_notas)
            media= sum(todas_notas)/numero_de_usuario
        else:
            numero_de_usuario= 0
            media = 0

        nota_usuario = NotaModel.query.filter_by(usuario_id=current_user.email,nome_jogo="God_Of_War").first()
        form = CadastrarNotaForm()
        form2 = AlterarNotaForm()
        if form.validate_on_submit():
            if nota_usuario is None:
                db.session.add(NotaModel(form.nota.data,"God_Of_War",current_user.email,form.comentario.data))
                db.session.commit()
                return redirect("/God_Of_War")
                
        if form2.validate_on_submit():
                nota_usuario.nota = form2.nota.data 
                nota_usuario.comentario = form2.comentario.data
                db.session.merge(nota_usuario)
                db.session.commit()
                return redirect("/God_Of_War") 
        return(render_template("God_Of_War.html", form=form,form2 = form2, nota_usuario=nota_usuario, media=media, todos_comentarios=todos_comentarios, lista_imagens=lista_imagens, todos_nomes=todos_nomes,numero_de_usuario=numero_de_usuario))
    
@app.route("/Minecraft",methods=['get', 'post'])
def Minecraft():
    if not current_user.is_authenticated:
        return redirect("/logar")
    elif current_user.is_authenticated:
        coments = NotaModel.query.filter_by(nome_jogo="Minecraft")
        todos_comentarios=[]
        todas_notas=[]
        todos_usuarios = []
        lista_imagens = []
        todos_nomes = []
        for i in coments:
            todos_comentarios.append(i.comentario)
            todas_notas.append(i.nota)
            todos_usuarios.append(i.usuario_id)
        for j in todos_usuarios:        
            usuarios = UserModel.query.filter_by(email=j).first()
            lista_imagens.append(usuarios.caminho_da_foto)
            todos_nomes.append(usuarios.nome)
        if len(todas_notas) != 0:
            numero_de_usuario=len(todas_notas)
            media= sum(todas_notas)/numero_de_usuario
        else:
            numero_de_usuario= 0
            media = 0

        nota_usuario = NotaModel.query.filter_by(usuario_id=current_user.email,nome_jogo="Minecraft").first()
        form = CadastrarNotaForm()
        form2 = AlterarNotaForm()
        if form.validate_on_submit():
            if nota_usuario is None:
                db.session.add(NotaModel(form.nota.data,"Minecraft",current_user.email,form.comentario.data))
                db.session.commit()
                return redirect("/Minecraft")
                
        if form2.validate_on_submit():
                nota_usuario.nota = form2.nota.data 
                nota_usuario.comentario = form2.comentario.data
                db.session.merge(nota_usuario)
                db.session.commit()
                return redirect("/Minecraft") 
        return(render_template("Minecraft.html", form=form,form2 = form2, nota_usuario=nota_usuario, media=media, todos_comentarios=todos_comentarios, lista_imagens=lista_imagens, todos_nomes=todos_nomes,numero_de_usuario=numero_de_usuario))

@login.user_loader
def load_user(email):
    return UserModel.query.filter_by(email=email).first()