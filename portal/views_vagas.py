from flask import (
    Blueprint,
    render_template,
    abort,
    url_for,
    request,
    redirect,
    jsonify
)
from flask_login import login_required, current_user
from portal.database import db
from portal.models import Vaga
from portal.decorators import role_required


vaga_bp=Blueprint("vagas",__name__, url_prefix="/vagas",template_folder="../templates/vagas")


@vaga_bp.route("/nova", methods=["GET", "POST"])
@login_required
@role_required("empresa")
def nova_vaga():

    empresa = Empresa.query.filter_by(usuario_id=current_user.id).first()

    if not empresa:
        flash("Perfil de empresa não encontrado.", "danger")
        return redirect(url_for("main.index"))

    if request.method == "POST":
        titulo = request.form["titulo"]
        descricao = request.form["descricao"]
        requisitos = request.form["requisitos"]
        localizacao = request.form["localizacao"]
        salario = request.form.get("salario")

        vaga = Vaga(
            titulo=titulo,
            descricao=descricao,
            requisitos=requisitos,
            localizacao=localizacao,
            salario=salario,
            empresa_id=empresa.id
        )

        db.session.add(vaga)
        db.session.commit()

        flash("Vaga publicada com sucesso!", "success")
        return redirect(url_for("main.index"))

    return render_template("vagas/nova.html.j2")


@vaga_bp.route("/vagas",methods=["GET"])
def listar_vagas():
    vagas = vaga.query.all()
    return jsonify([{
        "id": vaga.id,
        "titulo": vaga.titulo,
        "descricao": vaga.descricao
    } for vaga in vagas])

