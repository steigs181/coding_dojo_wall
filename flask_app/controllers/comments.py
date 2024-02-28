from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.comment import Comment

@app.route('/comment/create', methods = ['POST'])
def create_comment():
    Comment.save_comment(request.form)
    return redirect('/wall')