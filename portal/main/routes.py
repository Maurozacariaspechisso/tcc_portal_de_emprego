from flask import render_template
from portal.main import main_bp

@main_bp.route("/")
def index():
    return render_template("main/index.html.j2")


@main_bp.route("/vagas")
def vagas():
    return render_template("main/vagas.html.j2")


@main_bp.route("/sobre")
def sobre():
    return render_template("main/sobre.html.j2")
