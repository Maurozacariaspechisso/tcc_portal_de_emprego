from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from portal.models import Empresa, Vaga, Candidatura, Candidato
from portal.decorators import role_required

empresa_bp = Blueprint(
    "empresa",
    __name__,
    url_prefix="/empresa"
)



@empresa_bp.route("/dashboard")
@login_required
@role_required("empresa")
def dashboard():

    empresa = Empresa.query.filter_by(usuario_id=current_user.id).first()

    if not empresa:
        abort(404)

    vagas = Vaga.query.filter_by(empresa_id=empresa.id).all()

    return render_template(
        "empresa/dashboard.html.j2",
        vagas=vagas
    )



@empresa_bp.route("/candidato/<int:candidato_id>")
@login_required
@role_required("empresa")
def ver_candidato(candidato_id):

    empresa = Empresa.query.filter_by(usuario_id=current_user.id).first()

    if not empresa:
        abort(404)

    # ids das vagas das empresa
    vagas_ids = [vaga.id for vaga in empresa.vagas]

    # Ver se o candidato se candidatou a alguma vaga da empresa
    candidatura = Candidatura.query.filter(
        Candidatura.candidato_id == candidato_id,
        Candidatura.vaga_id.in_(vagas_ids)
    ).first()

    if not candidatura:
        abort(403)

    candidato = Candidato.query.get_or_404(candidato_id)
    usuario = candidato.usuario

    return render_template(
        "empresa/ver_candidato.html.j2",
        candidato=candidato,
        usuario=usuario,
        candidatura=candidatura
    )