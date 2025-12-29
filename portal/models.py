from portal.database import db
import datetime

class Usuario(db.Model):
   __tablename__ = 'usuarios'

   id = db.Column(db.Integer, primary_key=True)
   nome = db.Column(db.String(100), nullable=False)
   email = db.Column(db.String(120), unique=True, nullable=False)
   senha = db.Column(db.String(255), nullable=False)
   tipo = db.Column(db.String(50), nullable=False)  

   data_registro = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Candidato(db.Model):
    __tablename__ = "candidatos"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    telefone = db.Column(db.String(20))
    provincia = db.Column(db.String(50))
    area_interesse = db.Column(db.String(100))

    user = db.relationship("Usuarios", back_populates="candidatos")

    
    candidaturas = db.relationship("candidaturas", back_populates="candidatos", cascade="all, delete-orphan")

class Empresa(db.Model):
    __tablename__ = "empresas"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    nome_empresa = db.Column(db.String(120), nullable=False)
    localizacao = db.Column(db.String(120))
    descricao = db.Column(db.Text)

    user = db.relationship("usuarios", back_populates="empresas")

    vagas = db.relationship("vagas", back_populates="empresas",cascade="all, delete-orphan")



class Vagas(db.Model):
   __tablename__ = "vagas"
   id = db.Column(db.Integer,primary_key=True)
   empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'), nullable=False)
   titulo = db.Column(db.String(150), nullable=False)
   descricao = db.Column(db.Text, nullable=False)
   requisitos = db.Column(db.Text, nullable=False)
   localizacao = db.Column(db.String(150), nullable=False)
   salario = db.Column(db.String(100), nullable=True)
   data_postagem = db.Column(db.DateTime, default=datetime.datetime.utcnow)

   empresa = db.relationship("Empresas", back_populates="vagas")

   candidaturas = db.relationship("Candidaturas", back_populates="vagas", cascade="all, delete-orphan")


class Candidatura(db.Model):
    __tablename__ = "candidaturas"

    id = db.Column(db.Integer, primary_key=True)

    candidato_id = db.Column(db.Integer, db.ForeignKey("candidatos.id"), nullable=False)
    vaga_id = db.Column(db.Integer, db.ForeignKey("vagas.id"), nullable=False)
    data_candidatura = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    status = db.Column(db.String(50), default="pendente")  
    cv_path = db.Column(db.String(255))  

    candidato = db.relationship("Candidatos", back_populates="candidaturas")
    vaga = db.relationship("Vagas", back_populates="candidaturas")


