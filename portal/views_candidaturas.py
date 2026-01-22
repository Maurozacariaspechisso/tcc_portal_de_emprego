from flask import redirect, url_for, flash, request
from flask_login import login_required, current_user
from portal.database import db
from portal.models import Candidato, Vaga, Candidatura
from portal.decorators import role_required

@candidaturas_bp.route("/candidatar/<int:vaga_id>", methods=["POST"])
@login_required
@role_required("candidato")
def candidatar(vaga_id):

    candidato = Candidato.query.filter_by(
        usuario_id=current_user.id
    ).first()

    if not candidato:
        flash("Perfil de candidato não encontrado.", "danger")
        return redirect(url_for("vagas.listar_vagas"))

    vaga = Vaga.query.get_or_404(vaga_id)

    # evita candidatura duplicada
    existente = Candidatura.query.filter_by(
        candidato_id=candidato.id,
        vaga_id=vaga.id
    ).first()

    if existente:
        flash("Já se candidatou a esta vaga.", "warning")
        return redirect(url_for("vagas.listar_vagas"))

    candidatura = Candidatura(
        candidato_id=candidato.id,
        vaga_id=vaga.id,
        status="pendente"
    )

    db.session.add(candidatura)
    db.session.commit()

    flash("Candidatura enviada com sucesso!", "success")
    return redirect(url_for("candidaturas.minhas_candidaturas"))
