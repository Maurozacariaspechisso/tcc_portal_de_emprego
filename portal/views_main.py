from flask import Blueprint, redirect, url_for
from flask_login import current_user

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))

    if current_user.role == "candidato":
        return redirect(url_for("vagas.listar_vagas"))

    if current_user.role == "empresa":
        return redirect(url_for("empresa.dashboard"))

    return redirect(url_for("auth.login"))
