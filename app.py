from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
import os
import requests

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog-database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer)
    title = db.Column(db.String(250))
    body = db.Column(db.String(2000))








if __name__ == "__main__":
    app.run(debug=True)