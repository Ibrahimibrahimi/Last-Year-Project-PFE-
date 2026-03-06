from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# create the app and send it
def init_app() :
    from app.routes import main
    
    
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:1234@localhost:5432/shcooldb"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    app.register_blueprint(main)   
    
    return app