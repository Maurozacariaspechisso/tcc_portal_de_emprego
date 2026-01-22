from flask import (
    Blueprint,
    render_template,
    url_for,
    request,
    redirect,
    jsonify,
    flash,
    abort
)
from flask_login import login_required, current_user

from portal.database import db
from portal.models import Vaga, Empresa, Candidato, Candidatura
from portal.decorators import role_required


vaga_bp = Blueprint(
    "vagas",
    __name__,
    url_prefix="/vagas",
    template_folder="../templates/vagas"
)


# 1. LISTAR VAGAS 
@vaga_bp.route("/")
def listar_vagas():
    termo = request.args.get("q")

    query = Vaga.query

    if termo:
        query = query.filter(Vaga.titulo.ilike(f"%{termo}%"))

    vagas = query.order_by(Vaga.data_postagem.desc()).all()
    return render_template("vagas/listar.html.j2", vagas=vagas)



# 2. DETALHES DA VAGA

@vaga_bp.route("/<int:vaga_id>")
def detalhe_vaga(vaga_id):
    vaga = Vaga.query.get_or_404(vaga_id)
    return render_template("vagas/detalhe.html.j2", vaga=vaga)



# 3. CRIAR NOVA VAGA (EMPRESA)

@vaga_bp.route("/nova", methods=["GET", "POST"])
@login_required
@role_required("empresa")
def nova_vaga():

    empresa = Empresa.query.filter_by(usuario_id=current_user.id).first()

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
        return redirect(url_for("vagas.listar_vagas"))

    return render_template("vagas/nova.html.j2")



# 4. CANDIDATAR-SE A UMA VAGA (CANDIDATO)

@vaga_bp.route("/<int:vaga_id>/candidatar", methods=["POST"])
@login_required
@role_required("candidato")
def candidatar_vaga(vaga_id):

    vaga = Vaga.query.get_or_404(vaga_id)

    candidato = Candidato.query.filter_by(usuario_id=current_user.id).first()

    if not candidato:
        flash("Perfil de candidato não encontrado.", "danger")
        return redirect(url_for("vagas.listar_vagas"))

    # Evita candidatura duplicada
    candidatura_existente = Candidatura.query.filter_by(
        candidato_id=candidato.id,
        vaga_id=vaga.id
    ).first()

    if candidatura_existente:
        flash("Você já se candidatou a esta vaga.", "warning")
        return redirect(url_for("vagas.detalhe_vaga", vaga_id=vaga.id))

    candidatura = Candidatura(
        candidato_id=candidato.id,
        vaga_id=vaga.id
    )

    db.session.add(candidatura)
    db.session.commit()

    flash("Candidatura realizada com sucesso!", "success")
    return redirect(url_for("vagas.detalhe_vaga", vaga_id=vaga.id))



# 5. LISTAR CANDIDATURAS DA EMPRESA

@vaga_bp.route("/minhas/candidaturas")
@login_required
@role_required("empresa")
def candidaturas_empresa():

    empresa = Empresa.query.filter_by(usuario_id=current_user.id).first()

    if not empresa:
        abort(403)

    vagas = Vaga.query.filter_by(empresa_id=empresa.id).all()

    return render_template(
        "vagas/candidaturas_empresa.html.j2",
        vagas=vagas
    )



# 6. API JSON (OPCIONAL)

@vaga_bp.route("/api", methods=["GET"])
def vagas_api():
    vagas = Vaga.query.all()
    return jsonify([
        {
            "id": v.id,
            "titulo": v.titulo,
            "empresa_id": v.empresa_id
        }
        for v in vagas
    ])
