from flask import Flask
from portal.config import configure
from portal.views_vagas import vaga_bp
from portal.database import db
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from portal.views import  public_bp


login_manager = LoginManager()
login_manager.login_view = "auth.login"  # rota de login
login_manager.login_message = "Faça login para continuar."

def create_app():
    app = Flask(__name__)
    app.secret_key = "Malika#10"  # cheve secreta para sessões

    configure(app)
    
    from portal.views import public_bp
    app.register_blueprint(public_bp)

    login_manager.init_app(app)
    Bootstrap(app)


    from portal.auth import auth_bp
    app.register_blueprint(auth_bp)

    
    app.register_blueprint(vaga_bp)


    from portal import models  
    return app
