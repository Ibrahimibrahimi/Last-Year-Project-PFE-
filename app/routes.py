from flask import Flask , render_template , redirect , url_for , request 


# blueprint
from flask import Blueprint

main = Blueprint("main",__name__)



# ROUTES
@main.route("/")
def index():
    return "INDEX"

@main.route("/login")
def login():
    return "login"