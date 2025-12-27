import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def configure(app):
    # Configuracao da base de dados SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'portal.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Iniciando a nossa base de dados 
    from portal.database import configure as db_configure
    db_configure(app)
