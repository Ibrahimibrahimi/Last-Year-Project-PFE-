from flask_sqlalchemy import SQLAlchemy
from . import db


class User(db.Model) :
    __tablename__ = "user"
    
    # attributes
    id = db.Column(db.Integer,autoincrement = True)
    name = db.Column(db.String(30),nullable=False)

