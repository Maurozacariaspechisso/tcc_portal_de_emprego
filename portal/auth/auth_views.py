from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from portal.database import db
from portal.models import Usuario
from portal.app import login_manager


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")
