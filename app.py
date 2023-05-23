from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
import os
import requests

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog-database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# api_url_user_IDs = f"https://jsonplaceholder.typicode.com/users"
# user_IDs = requests.get(api_url_user_IDs)
# print(user_IDs)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer)
    title = db.Column(db.String(250))
    body = db.Column(db.String(2000))

    @staticmethod
    def validate_userID(userID):
        url = f"https://jsonplaceholder.typicode.com/users/{userID}"
        response = requests.get(url)

        if response.status_code == 200:
            return True
        else:
            return False
    
    def save(self):
        if self.validate_userID(self.userID):
            db.session.add(self)
            db.session.commit()
            return True
        else:
            return False






if __name__ == "__main__":
    app.run(debug=True)