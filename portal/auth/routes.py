from flask import Blueprint, render_template,redirect,url_for,flash,request
from portal.database import db
from portal.models import Usuario
from flask_login import logout_user

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
        tipo = request.form["tipo"]

        if Usuario.query.filter_by(email=email).first():
            flash("Email já registrado. Por favor, use outro email.")
            return redirect(url_for("auth.register"))

        usuario = Usuario(nome=nome, email=email, tipo=tipo)
        usuario.set_password(senha)
        db.session.add(usuario)
        db.session.commit()

        flash("Formulario enviado com sucesso!", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html.j2")





@auth_bp.route("/logout")
def logout():
    logout_user()
    flash("Sessão encerrada.", "info")
    return redirect(url_for("auth.login"))

