from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()


def configure(app):
    db.init_app(app)
    Migrate(app, db)
    return app


