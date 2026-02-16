from flask import Blueprint, render_template
from flask_login import login_required, current_user
from portal.models import Empresa, Vaga
from portal.decorators import role_required

empresa_bp = Blueprint(
    "empresa",          # ⚠️ ESTE NOME É CRÍTICO
    __name__,
    url_prefix="/empresa"
)

@empresa_bp.route("/dashboard")
@login_required
@role_required("empresa")
def dashboard():
    empresa = Empresa.query.filter_by(usuario_id=current_user.id).first()
    vagas = Vaga.query.filter_by(empresa_id=empresa.id).all()
    return render_template("empresa/dashboard.html.j2", vagas=vagas)
