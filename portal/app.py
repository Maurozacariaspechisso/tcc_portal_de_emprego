from flask import Flask
from portal.config import configure
from portal.views import vaga_bp
from portal.database import db
from flask_login import LoginManager
from flask_bootstrap import Bootstrap



login_manager = LoginManager()
login_manager.login_view = "auth.login"  # rota de login
login_manager.login_message = "Faça login para continuar."

def create_app():
    app = Flask(__name__)
    app.secret_key = "Malika#10"  # cheve secreta para sessões

    configure(app)
    db.init_app(app)

    login_manager.init_app(app)
    Bootstrap(app)
    
    from portal.auth.views import auth_bp
    app.register_blueprint(vaga_bp)


    from portal import models  
    return app
