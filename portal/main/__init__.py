from flask import Blueprint

main_bp = Blueprint(
    "main",
    __name__
)

from portal.main import routes
