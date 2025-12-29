from flask import Flask
from portal.config import configure
from portal.views import vaga_bp

def create_app():
    app = Flask(__name__)
    configure(app)
    app.register_blueprint(vaga_bp)
    from portal import models  
    return app
