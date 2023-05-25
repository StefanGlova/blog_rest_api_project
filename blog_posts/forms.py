from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired

class AddBlog(FlaskForm):
    userID = IntegerField("userID", validators=[DataRequired()])
    title = StringField("title", validators=[DataRequired()])
    body = TextAreaField("body", validators=[DataRequired()])
    submit = SubmitField("submit")


class ShowBlogById(FlaskForm):
    id = IntegerField("id", validators=[DataRequired()])
    submit = SubmitField("submit")


class ShowBlogByUserId(FlaskForm):
    userID = IntegerField("userID", validators=[DataRequired()])
    submit = SubmitField("submit")


class DeleteBlog(FlaskForm):
    id = IntegerField("id", validators=[DataRequired()])
    submit = SubmitField("submit")


class UpdateTitle(FlaskForm):
    id = IntegerField("id", validators=[DataRequired()])
    title = StringField("title", validators=[DataRequired()])
    submit = SubmitField("submit")


class UpdateBody(FlaskForm):
    id = IntegerField("id", validators=[DataRequired()])
    body = TextAreaField("body", validators=[DataRequired()])
    submit = SubmitField("submit")
