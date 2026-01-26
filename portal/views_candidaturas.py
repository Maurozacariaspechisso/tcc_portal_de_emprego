from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from portal.database import db
from portal.models import Candidato, Empresa, Vaga, Candidatura
from portal.decorators import role_required

candidaturas_bp = Blueprint(
    "candidaturas",
    __name__,
    url_prefix="/candidaturas"
)

# =========================================================
# CANDIDATO – CANDIDATAR-SE A UMA VAGA
# =========================================================
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

    candidatura_existente = Candidatura.query.filter_by(
        candidato_id=candidato.id,
        vaga_id=vaga.id
    ).first()

    if candidatura_existente:
        flash("Já se candidatou a esta vaga.", "warning")
        return redirect(url_for("vagas.listar_vagas"))

    nova_candidatura = Candidatura(
        candidato_id=candidato.id,
        vaga_id=vaga.id,
        status="pendente"
    )

    db.session.add(nova_candidatura)
    db.session.commit()

    flash("Candidatura enviada com sucesso!", "success")
    return redirect(url_for("candidaturas.minhas_candidaturas"))


# =========================================================
# CANDIDATO – MINHAS CANDIDATURAS
# =========================================================
@candidaturas_bp.route("/minhas")
@login_required
@role_required("candidato")
def minhas_candidaturas():

    candidato = Candidato.query.filter_by(
        usuario_id=current_user.id
    ).first()

    if not candidato:
        flash("Perfil de candidato não encontrado.", "danger")
        return redirect(url_for("main.index"))

    candidaturas = (
        Candidatura.query
        .filter_by(candidato_id=candidato.id)
        .order_by(Candidatura.id.desc())
        .all()
    )

    return render_template(
        "candidaturas/minhas.html.j2",
        candidaturas=candidaturas
    )


# =========================================================
# EMPRESA – LISTAR CANDIDATURAS DAS SUAS VAGAS
# =========================================================
@candidaturas_bp.route("/empresa")
@login_required
@role_required("empresa")
def candidaturas_empresa():

    empresa = Empresa.query.filter_by(
        usuario_id=current_user.id
    ).first()

    if not empresa:
        flash("Perfil da empresa não encontrado.", "danger")
        return redirect(url_for("main.index"))

    candidaturas = (
        Candidatura.query
        .join(Vaga)
        .filter(Vaga.empresa_id == empresa.id)
        .order_by(Candidatura.id.desc())
        .all()
    )

    return render_template(
        "candidaturas/empresa.html.j2",
        candidaturas=candidaturas
    )


# =========================================================
# EMPRESA – ACEITAR CANDIDATURA
# =========================================================
@candidaturas_bp.route("/<int:id>/aceitar", methods=["POST"])
@login_required
@role_required("empresa")
def aceitar_candidatura(id):

    candidatura = Candidatura.query.get_or_404(id)

    empresa = Empresa.query.filter_by(
        usuario_id=current_user.id
    ).first()

    if candidatura.vaga.empresa_id != empresa.id:
        flash("Ação não permitida.", "danger")
        return redirect(url_for("candidaturas.candidaturas_empresa"))

    candidatura.status = "aceite"
    db.session.commit()

    flash("Candidatura aceite com sucesso.", "success")
    return redirect(url_for("candidaturas.candidaturas_empresa"))


# =========================================================
# EMPRESA – REJEITAR CANDIDATURA
# =========================================================
@candidaturas_bp.route("/<int:id>/rejeitar", methods=["POST"])
@login_required
@role_required("empresa")
def rejeitar_candidatura(id):

    candidatura = Candidatura.query.get_or_404(id)

    empresa = Empresa.query.filter_by(
        usuario_id=current_user.id
    ).first()

    if candidatura.vaga.empresa_id != empresa.id:
        flash("Ação não permitida.", "danger")
        return redirect(url_for("candidaturas.candidaturas_empresa"))

    candidatura.status = "rejeitada"
    db.session.commit()

    flash("Candidatura rejeitada.", "warning")
    return redirect(url_for("candidaturas.candidaturas_empresa"))
