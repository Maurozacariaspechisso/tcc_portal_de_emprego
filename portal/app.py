from flask import Flask,render_template
from portal.config import configure
from portal.database import db
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    configure(app)
    return app
    
    