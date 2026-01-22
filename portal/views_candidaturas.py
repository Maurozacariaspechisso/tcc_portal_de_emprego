from flask import Blueprint, render_template
from flask_login import login_required, current_user
from portal.models import Candidato, Candidatura
from portal.decorators import role_required

candidaturas_bp = Blueprint(
    "candidaturas",
    __name__,
    url_prefix="/candidaturas",
    template_folder="../templates/candidaturas"
)


@candidaturas_bp.route("/minhas")
@login_required
@role_required("candidato")
def minhas_candidaturas():

    candidato = Candidato.query.filter_by(
        usuario_id=current_user.id
    ).first()

    if not candidato:
        return render_template(
            "candidaturas/minhas.html.j2",
            candidaturas=[]
        )

    candidaturas = Candidatura.query.filter_by(
        candidato_id=candidato.id
    ).order_by(Candidatura.data_candidatura.desc()).all()

    return render_template(
        "candidaturas/minhas.html.j2",
        candidaturas=candidaturas
    )
