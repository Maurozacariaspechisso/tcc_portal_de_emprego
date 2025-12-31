from flask import render_template, redirect, url_for
from portal.auth import auth_bp

@auth_bp.route("/login")
def login():
    return render_template("auth/login.html")
