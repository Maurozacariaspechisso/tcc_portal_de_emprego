from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request
)
from flask_login import login_required, current_user

from portal.database import db
from portal.models import Vaga, Empresa, Candidatura
from portal.decorators import role_required

# Blueprint
vagas_bp = Blueprint(
    "vagas",
    __name__,
    url_prefix="/vagas"
)


#  LISTAR TODAS AS VAGAS (PÚBLICO / CANDIDATO)

@vagas_bp.route("/")
def listar_vagas():
    termo = request.args.get("q")

    query = Vaga.query.order_by(Vaga.data_postagem.desc())

    if termo:
        query = query.filter(
            Vaga.titulo.ilike(f"%{termo}%") |
            Vaga.localizacao.ilike(f"%{termo}%")
        )

    vagas = query.all()

    return render_template("vagas/listar.html.j2", vagas=vagas)


#  DETALHE DA VAGA
@vagas_bp.route("/<int:vaga_id>")
def detalhe_vaga(vaga_id):
    vaga = Vaga.query.get_or_404(vaga_id)
    return render_template("vagas/detalhe.html.j2", vaga=vaga)



#  CRIAR NOVA VAGA (EMPRESA)
@vagas_bp.route("/nova", methods=["GET", "POST"])
@login_required
@role_required("empresa")
def nova_vaga():

    empresa = Empresa.query.filter_by(
        usuario_id=current_user.id
    ).first()

    if not empresa:
        flash("Perfil de empresa não encontrado.", "danger")
        return redirect(url_for("main.index"))

    if request.method == "POST":
        vaga = Vaga(
            titulo=request.form["titulo"],
            descricao=request.form["descricao"],
            requisitos=request.form["requisitos"],
            localizacao=request.form["localizacao"],
            salario=request.form.get("salario"),
            empresa_id=empresa.id
        )

        db.session.add(vaga)
        db.session.commit()

        flash("Vaga publicada com sucesso!", "success")
        return redirect(url_for("vagas.minhas_vagas"))

    return render_template("vagas/nova.html.j2")



#  VAGAS DA EMPRESA LOGADA
@vagas_bp.route("/minhas")
@login_required
@role_required("empresa")
def minhas_vagas():

    empresa = Empresa.query.filter_by(
        usuario_id=current_user.id
    ).first()

    if not empresa:
        flash("Perfil de empresa não encontrado.", "danger")
        return redirect(url_for("main.index"))

    vagas = Vaga.query.filter_by(
        empresa_id=empresa.id
    ).all()

    return render_template(
        "vagas/minhas.html.j2",
        vagas=vagas
    )



#CANDIDATURAS PARA UMA VAGA (EMPRESA)

@vagas_bp.route("/<int:vaga_id>/candidaturas")
@login_required
@role_required("empresa")
def candidaturas_vaga(vaga_id):

    vaga = Vaga.query.get_or_404(vaga_id)

    empresa = Empresa.query.filter_by(
        usuario_id=current_user.id
    ).first()

    if vaga.empresa_id != empresa.id:
        flash("Acesso não autorizado.", "danger")
        return redirect(url_for("vagas.minhas_vagas"))

    candidaturas = (
        Candidatura.query
        .filter_by(vaga_id=vaga.id)
        .all()
    )

    return render_template(
        "vagas/candidaturas_empresa.html.j2",
        vaga=vaga,
        candidaturas=candidaturas
    )
