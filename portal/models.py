from flask_login import UserMixin
from portal.database import db
from datetime import datetime
from portal.database import db
from portal.extensions import  login_manager
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(UserMixin, db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    data_registro = db.Column(db.DateTime, default=datetime.utcnow)

    role = db.Column(db.String(20), nullable=False)  # candidato | empresa

    candidato = db.relationship(
        "Candidato",
        back_populates="usuario",
        uselist=False,
        cascade="all, delete-orphan"
    )

    empresa = db.relationship(
        "Empresa",
        back_populates="usuario",
        uselist=False,
        cascade="all, delete-orphan"
    )

    def set_password(self, senha):
        self.senha = generate_password_hash(senha)

    def check_password(self, senha):
        return check_password_hash(self.senha, senha)


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


class Candidato(db.Model):
    __tablename__ = "candidatos"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        unique=True,
        nullable=False
    )

    telefone = db.Column(db.String(20))
    provincia = db.Column(db.String(50))
    area_interesse = db.Column(db.String(100))

    
    usuario = db.relationship("Usuario", back_populates="candidato")
    candidaturas = db.relationship(
        "Candidatura",
        back_populates="candidato",
        cascade="all, delete-orphan"
    )

class Empresa(db.Model):
    __tablename__ = "empresas"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        unique=True,
        nullable=False
    )

    nome_empresa = db.Column(db.String(120), nullable=False)
    localizacao = db.Column(db.String(120))
    descricao = db.Column(db.Text)

    usuario = db.relationship("Usuario", back_populates="empresa")
    vagas = db.relationship(
        "Vaga",
        back_populates="empresa",
        cascade="all, delete-orphan"
    )
class Vaga(db.Model):
    __tablename__ = "vagas"

    id = db.Column(db.Integer, primary_key=True)
    empresa_id = db.Column(
        db.Integer,
        db.ForeignKey("empresas.id"),
        nullable=False
    )

    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    requisitos = db.Column(db.Text, nullable=False)
    localizacao = db.Column(db.String(150), nullable=False)
    salario = db.Column(db.String(100))
    data_postagem = db.Column(db.DateTime, default=datetime.utcnow)

    empresa = db.relationship("Empresa", back_populates="vagas")
    candidaturas = db.relationship(
        "Candidatura",
        back_populates="vaga",
        cascade="all, delete-orphan"
    )


class Candidatura(db.Model):
    __tablename__ = "candidaturas"

    id = db.Column(db.Integer, primary_key=True)
    candidato_id = db.Column(
        db.Integer,
        db.ForeignKey("candidatos.id"),
        nullable=False
    )
    vaga_id = db.Column(
        db.Integer,
        db.ForeignKey("vagas.id"),
        nullable=False
    )

    data_candidatura = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default="pendente")
    cv_path = db.Column(db.String(255))

    candidato = db.relationship("Candidato", back_populates="candidaturas")
    vaga = db.relationship("Vaga", back_populates="candidaturas")

