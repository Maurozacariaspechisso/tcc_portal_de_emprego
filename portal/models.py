from database import configure
import datetime

class usuario(db.model):
   __tablename__ = 'usuario'

   id = db.Column(db.Integer, primary_key=True)
   nome = db.Column(db.String(100), nullable=False)
   email = db.Column(db.String(120), unique=True, nullable=False)
   senha = db.Column(db.String(255), nullable=False)
   tipo = db.Column(db.String(50), nullable=False)  

   data_registro = db.Column(db.DateTime, default=datetime.utcnow)

class Candidato(db.Model):
    __tablename__ = "candidatos"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    telefone = db.Column(db.String(20))
    provincia = db.Column(db.String(50))
    area_interesse = db.Column(db.String(100))

    user = db.relationship("User", back_populates="candidato")

    
    candidaturas = db.relationship("Candidatura", back_populates="candidato", cascade="all, delete-orphan")

class Empresa(db.Model):
    __tablename__ = "empresas"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    nome_empresa = db.Column(db.String(120), nullable=False)
    localizacao = db.Column(db.String(120))
    descricao = db.Column(db.Text)

    user = db.relationship("User", back_populates="empresa")

    vagas = db.relationship("Vaga", back_populates="empresa",cascade="all, delete-orphan")



class vagas(db.Model):
   __tablename__ = "vagas"
   id = db.Column(db.Integer,primary_key=True)
   empresa_id = db.Column(db.Integer, db.ForeignKey('empresa.id'), nullable=False)
   titulo = db.Column(db.String(150), nullable=False)
   descricao = db.Column(db.Text, nullable=False)
   requisitos = db.Column(db.Text, nullable=False)
   localizacao = db.Column(db.String(150), nullable=False)
   salario = db.Column(db.String(100), nullable=True)
   data_postagem = db.Column(db.DateTime, default=datetime.utcnow)

   empresa = db.relationship("Empresa", back_populates="vagas")

   candidaturas = db.relationship("Candidatura", back_populates="vaga", cascade="all, delete-orphan")


class Candidatura(db.Model):
    __tablename__ = "candidaturas"

    id = db.Column(db.Integer, primary_key=True)

    candidato_id = db.Column(db.Integer, db.ForeignKey("candidatos.id"), nullable=False)
    vaga_id = db.Column(db.Integer, db.ForeignKey("vagas.id"), nullable=False)
    data_candidatura = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default="pendente")  # pendente / aceite / rejeitado
    cv_path = db.Column(db.String(255))  # caminho do arquivo do currículo

    candidato = db.relationship("Candidato", back_populates="candidaturas")
    vaga = db.relationship("Vaga", back_populates="candidaturas")