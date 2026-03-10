from . import main_bp
from flask_login import login_required
from flask import render_template


@main_bp.route("/home")
@login_required
def home():
    return render_template("home.html")