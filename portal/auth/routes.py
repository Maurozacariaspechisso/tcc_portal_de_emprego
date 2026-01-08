from flask import Blueprint, render_template,redirect,url_for,flash,request,abort
from portal.database import db
from portal.models import Usuario ,Candidato ,Empresa
from flask_login import login_user, logout_user, login_required,current_user
from werkzeug.security import generate_password_hash


auth_bp = Blueprint(
    "auth",
    __name__,
    template_folder="../templates/auth",
    url_prefix="/auth"
)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        usuario = Usuario.query.filter_by(email=email).first()
        if not usuario or not usuario.check_password(senha):
            flash("Email ou senha inválidos. Tente novamente.", "danger")
            return redirect(url_for("auth.login"))

        login_user(usuario)

        flash("Login realizado com sucesso!", "success")
        return redirect(url_for("main.index"))
    return render_template("login.html.j2")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]
        tipo = request.form["tipo"]  # candidato | empresa

        # valida email duplicado
        if Usuario.query.filter_by(email=email).first():
            flash("Email já cadastrado", "danger")
            return redirect(url_for("auth.register"))

        # cria usuário
        usuario = Usuario(
            email=email,
            role=tipo
        )
        usuario.set_password(senha)

        db.session.add(usuario)
        db.session.commit()

        # cria perfil conforme o papel
        if tipo == "candidato":
            perfil = Candidato(nome=nome, usuario_id=usuario.id)
        elif tipo == "empresa":
            perfil = Empresa(nome=nome, usuario_id=usuario.id)
        else:
            abort(400)

        db.session.add(perfil)
        db.session.commit()

        flash("Conta criada com sucesso", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html.j2")



@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sessão encerrada.", "info")
    return redirect(url_for("auth.login"))

