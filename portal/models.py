from portal.database import db
from datetime import datetime


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # 'candidato' ou 'recrutador'
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    candidatos = db.relationship("Candidato", backref="usuario", lazy=True)


class Candidato(db.Model):
    __tablename__ = "candidatos"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    telefone = db.Column(db.String(20))
    endereco = db.Column(db.String(200))
    area_interesse = db.Column(db.String(100))

    usuario = db.relationship("Usuario", backref=db.backref("candidato", uselist=False))
    candidaturas = db.relationship("Candidatura", backref="candidato", lazy=True)

class Empresa(db.Model):
    __tablename__ = "empresas"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    localizacao = db.Column(db.String(200))
    descricao = db.Column(db.Text)

    usuario = db.relationship("Usuario", backref=db.backref("empresa", uselist=False))
    vagas = db.relationship("Vagas", backref="empresa", lazy=True)

class Vaga(db.Model):
    __tablename__ = "vagas"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    localizacao = db.Column(db.String(200))
    requisitos = db.Column(db.Text)
    empresa_id = db.Column(db.Integer, db.ForeignKey("empresas.id"), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    empresa = db.relationship("Empresa", backref=db.backref("vagas_empresa", lazy=True))
    candidaturas = db.relationship("Candidatura", backref="vaga", lazy=True)

class Candidatura(db.Model):
    __tablename__ = "candidaturas"

    id = db.Column(db.Integer, primary_key=True)
    candidato_id = db.Column(db.Integer, db.ForeignKey("candidatos.id"), nullable=False)
    vaga_id = db.Column(db.Integer, db.ForeignKey("vagas.id"), nullable=False)
    data_candidatura = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default="Pendente")  # Pendente, Aceito, Rejeitado
    cv_path = db.Column(db.String(200))  

    candidato = db.relationship("Candidato", backref=db.backref("candidaturas_candidato", lazy=True))
    vaga = db.relationship("Vaga", backref=db.backref("candidaturas_vaga", lazy=True))

