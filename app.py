from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource, fields, reqparse
import requests


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog-database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
api = Api(app)

external_api_url = "https://jsonplaceholder.typicode.com"

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer)
    title = db.Column(db.String(250))
    body = db.Column(db.String(2000))

blog_model = api.model("Blog", {
    "id": fields.Integer(readonly=True),
    "userID": fields.Integer(required=True),
    "title": fields.String(required=True),
    "body": fields.String(required=True)
})

@api.route("/blogs")
class BlogResource(Resource):
    @api.doc("list_blogs")
    def get(self):
        """
        Get a list of all blogs.
        """
        blogs = BlogPost.query.all()
        return [{"id": blog.id, 
                 "userID": blog.userID, 
                 "title": blog.title, 
                 "body": blog.body} for blog in blogs]
    
    @api.doc("create_blog")
    @api.expect(blog_model)
    def post(self):
        """
        Create a new blog post.
        """
        args = api.payload
        new_blog = BlogPost(userID=args["userID"], 
                            title=args["title"], 
                            body=args["body"])
        db.session.add(new_blog)        
        db.session.commit()
        return {"message": "Blog added successfully"}, 201

@api.route("/blogs/<int:blog_id>")
class BlogRescource(Resource):
    """
    Represents a single blog post.
    """

    @api.doc("get_blog")
    def get(self, blog_id):
        """
        Get a blog by ID.
        """
        blog = BlogPost.query.get(blog_id)
        if not blog:
            response = requests.get(f"{external_api_url}/posts/{blog_id}")
            if response.status_code == 200:
                external_blog = response.json()
                return external_blog
            return {"error": "Blog not found"}, 404
        return {"id": blog.id, 
                "userID": blog.userID,
                "title": blog.title, 
                "body": blog.body}
    
    @api.doc("update_blog")
    @api.expect(blog_model)
    def put(self, blog_id):
        """
        Update a blog by ID.
        """
        args = api.payload
        blog = BlogPost.query.get(blog_id)
        if not blog:
            return {"error": "Blog not found"}, 404
        blog.userID = args["userID"]
        blog.title = args["title"]
        blog.body = args["body"]
        db.session.commit()
        return {"message": "Blog updated successfully"}
    
    @api.doc("delete_blog")
    def delete(self, blog_id):
        """
        Delete a blog by ID.
        """
        blog = BlogPost.query.get(blog_id)
        if not blog:
            return {"error": "Blog not found"}, 404
        db.session.delete(blog)
        db.session.commit()
        return {"message": "Blog deleted successfully"}

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

