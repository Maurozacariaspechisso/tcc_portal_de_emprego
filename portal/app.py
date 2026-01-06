from flask import Flask
from portal.config import configure
from portal.views_vagas import vaga_bp
from portal.database import db,migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from portal.extensions import login_manager



def create_app():
    app = Flask(__name__)
    app.secret_key = "Malika#10"  # cheve secreta para sessões

    configure(app)
    
    login_manager.init_app(app)
    Bootstrap(app)

    from portal.main import main_bp
    from portal.auth import auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp,url_prefix="/auth")

    
    app.register_blueprint(vaga_bp)


    from portal import models  
    return app
