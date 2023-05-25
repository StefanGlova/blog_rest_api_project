from flask import Flask, render_template, request, jsonify
from blog_posts.forms import AddBlog, ShowBlogById, ShowBlogByUserId, DeleteBlog, UpdateBody, UpdateTitle
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
import requests


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog-database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = "abc159qwe951"
db = SQLAlchemy(app)
SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.json"
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config = {
        "app_name": "blog_posts"
    }
)

app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix = SWAGGER_URL)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer)
    title = db.Column(db.String(250))
    body = db.Column(db.String(2000))

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddBlog()
    if request.method == "POST":
        if form.validate_on_submit():
            new_blog = BlogPost(
                userID = form.userID.data,
                title = form.title.data,
                body = form.body.data
            )
            url = f"https://jsonplaceholder.typicode.com/users/{new_blog.userID}"
            response = requests.get(url)

            if response.status_code == 200:
                db.session.add(new_blog)
                db.session.commit()
                return render_template("success.html", message = "Blog added sucessfully")
            else:
                return render_template("error.html", error="User does not exist")
    else:
        return render_template("add.html", form=form)


@app.route("/delete", methods=["GET", "POST"])
def delete_blog():
    form = DeleteBlog()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                id = form.id.data
                blog = BlogPost.query.get(id)
                if blog:
                    db.session.delete(blog)
                    db.session.commit()
                    return render_template("success.html", message = "Blog deleted successfully")
                else:
                    raise TypeError
        except TypeError:
            return render_template("error.html", error = "Blog does not exist")
    else:
        return render_template("delete.html", form=form)


@app.route("/viewID", methods=["GET", "POST"])
def show_blog_by_ID():
    form = ShowBlogById()
    if request.method == "POST":
        if form.validate_on_submit():
            id = form.id.data
            blog = BlogPost.query.get(id)
            if blog:
                return jsonify({
                    "id": blog.id,
                    "userID": blog.userID,
                    "title": blog.title,
                    "body": blog.body
                })
            else:
                api_url = f"https://jsonplaceholder.typicode.com/posts/{id}"
                try:
                    response = requests.get(api_url)
                    if response.status_code == 200:
                        external_blog = response.json()
                        return jsonify(external_blog)
                    else:
                        return render_template("error.html", error="Blog not found even externally")
                except requests.exceptions.RequestException:
                    return render_template("error.html", error="Failed to get blog from external API")
    else:
        return render_template("viewID.html", form=form)


@app.route("/viewUser", methods=["GET", "POST"])
def show_blog_from_user():
    form = ShowBlogByUserId()
    if request.method == "POST": 
        try:
            if form.validate_on_submit():
                userID = form.userID.data
                blog = BlogPost.query.filter_by(userID=userID).first()
                if blog:
                    return jsonify({
                        "id": blog.id,
                        "userID": blog.userID,
                        "title": blog.title,
                        "body": blog.body
                    })
                else:
                    raise TypeError
        except TypeError:
            return render_template("error.html", error="Blog not found for give User")
    else:
        return render_template("viewUser.html", form=form)

@app.route("/updateTitle", methods=["GET", "POST"])
def update_blog_title():
    form = UpdateTitle()
    if request.method == "POST":
        if form.validate_on_submit():
            id = form.id.data
            blog = BlogPost.query.get(id)
            if blog:
                blog.title = form.title.data
                db.session.commit()
                return render_template("success.html", message="Title updated successfully")
            else:
                return render_template("error.html", error="Blog not found - title can't be changed")
    else:
        return render_template("updateTitle.html", form=form)    

@app.route("/updateBody", methods=["GET", "POST"])
def update_blog_body():
    form = UpdateBody()
    if request.method == "POST":
        if form.validate_on_submit():
            id = form.id.data
            blog = BlogPost.query.get(id)
            if blog:
                blog.body = form.body.data
                db.session.commit()
                return render_template("success.html", message="Blog text updated successfully")
            else:
                return render_template("error.html", error="Blog not found - text can't be changed")
    else:
        return render_template("updateBody.html", form=form) 


if __name__ == "__main__":
    app.run(debug=True)