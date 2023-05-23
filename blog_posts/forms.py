from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired
import requests
# from app import db

# form to add new blog + validate userID form external API
class AddBlog(FlaskForm):
    userID = IntegerField("userID", validators=[DataRequired()])
    title = StringField("title", validators=[DataRequired()])
    body = TextAreaField("body", validators=[DataRequired()])
    submit = SubmitField("submit")

    # @staticmethod
    # def validate_userID(userID):
    #     url = f"https://jsonplaceholder.typicode.com/users/{userID}"
    #     response = requests.get(url)

    #     if response.status_code == 200:
    #         return True
    #     else:
    #         return False
    
    # def save(self):
    #     if self.validate_userID(self.userID):
    #         db.session.add(self)
    #         db.session.commit()
    #         return True
    #     else:
    #         return False


# form to show blog by id 
# TODO implement on route - if not found, use external API
class ShowBlogById(FlaskForm):
    id = IntegerField("id", validators=[DataRequired()])
    submit = SubmitField("submit")


# form to show blog by userID
# TODO implement on route - if not found, raise error message
class ShowBlogByUserId(FlaskForm):
    userID = IntegerField("userID", validators=[DataRequired()])
    submit = SubmitField("submit")

# form to delete blog
# TODO implement on route - if not found, raise error message
class DeleteBlog(FlaskForm):
    id = IntegerField("id", validators=[DataRequired()])
    submit = SubmitField("submit")

# form to change title of blog
# TODO implement on route - if not found, raise error message
class UpdateTitle(FlaskForm):
    id = IntegerField("id", validators=[DataRequired()])
    title = StringField("title", validators=[DataRequired()])
    submit = SubmitField("submit")

# form to change body of blog
# TODO implement on route - if not found, raise error message
class UpdateBody(FlaskForm):
    id = IntegerField("id", validators=[DataRequired()])
    body = TextAreaField("id", validators=[DataRequired()])
    submit = SubmitField("submit")