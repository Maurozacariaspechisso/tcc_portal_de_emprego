from flask import Blueprint

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    return "Portal de Emprego a funcionar"
