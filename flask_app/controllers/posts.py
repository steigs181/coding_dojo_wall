from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.post import Post
from flask_app.models.user import User
from flask_app.models.comment import Comment
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/wall')
def home():
    user = User.get_one(session['user_id'])
    posts = Post.get_all_posts_with_comments()
    return render_template('wall.html', user = user, posts = posts)

@app.route('/create/post', methods=["POST"])
def createPost():
    if not Post.is_post_valid(request.form):
        return redirect('/wall')
    data = {
        "content": request.form['content'],
        "user_id": session['user_id']
    }
    Post.create_post(data)
    return redirect('/wall')

@app.route ('/wall/post/delete/<int:post_id>')
def delete_post(post_id):
    Post.delete(post_id)
    return redirect ('/wall')