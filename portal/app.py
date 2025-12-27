from flask import Flask
from portal.config import configure

def create_app():
    app = Flask(__name__)
    configure(app)
    from portal import models  
    return app
