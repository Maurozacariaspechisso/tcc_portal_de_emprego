from flask import (
    Blueprint,
    render_template,
    abort,
    url_for,
    request,
    redirect,
    jsonify
)
from portal.database import db
from portal.models import Vaga


vaga_bp=Blueprint("vagas",__name__, template_folder ="template")

@vaga_bp.route("/vagas",methods=["POST","GET"])
def criar_vaga():
    data = request.json
    vaga = Vagas(
        titulo=data["titulo"],
        descricao=data["descricao"]
    )
    db.session.add(vaga)
    db.session.commit()
    return jsonify({"message":"Vaga criada com sucesso!"}),201

@vaga_bp.route("/vagas",methods=["GET"])
def listar_vagas():
    vagas = vaga.query.all()
    return jsonify([{
        "id": vaga.id,
        "titulo": vaga.titulo,
        "descricao": vaga.descricao
    } for vaga in vagas])

