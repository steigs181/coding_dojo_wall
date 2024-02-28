# from user import User
from flask import flash
from flask_app.models.user import User
from flask_app.models.comment import Comment
from flask_app.config.mysqlconnection import connectToMySQL

class Post:

    DB = "coding_dojo_wall_schema"

    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.user_id = data["user_id"]
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.comments = []
        self.owner = None

    # VALIDATION
    @staticmethod
    def is_post_valid(post):
        is_valid = True
        if len(post['content']) < 1:
            is_valid = False
            flash('Post content cannot be blank')
        return is_valid


    # CREATE
    @classmethod
    def create_post(cls, data):
        query = """
                INSERT INTO posts (content, user_id, created_at, updated_at)
                VALUES (%(content)s, %(user_id)s, NOW(), NOW())
                """
        results = connectToMySQL(cls.DB).query_db(query,data)
        return results
    
    # READ
    @classmethod
    def get_all_posts_with_comments(cls):
        query = """
                SELECT * FROM posts JOIN users on posts.user_id = users.id 
                LEFT JOIN comments ON comments.post_id = posts.id
                ORDER BY posts.created_at DESC;
                """
        results = connectToMySQL(cls.DB).query_db(query)
        all_posts = []
        for row_from_db in results:
            one_post = cls(row_from_db)
            post_creator = {
            "id": row_from_db['users.id'],
            "first_name": row_from_db['first_name'],
            "last_name": row_from_db['last_name'],
            "email": row_from_db['email'],
            "password": row_from_db['password'],
            "created_at": row_from_db['created_at'],
            "updated_at": row_from_db['updated_at']
            }
            creator = User(post_creator)
            one_post.owner = creator
            if row_from_db['comments.id'] is not None:
                comment_data = {
                "id": row_from_db['comments.id'],
                'user_id': row_from_db['comments.user_id'],
                'post_id': row_from_db['post_id'],
                "content": row_from_db['comments.content'],
                'created_at': row_from_db['comments.created_at'],
                "updated_at": row_from_db['comments.updated_at']
                }
                comment = Comment(comment_data)
                one_post.comments.append(comment)
            all_posts.append(one_post)
        return all_posts
    

    #DELETE
    @classmethod
    def delete(cls, post_id):
        query = """
                DELETE FROM posts WHERE id = %(id)s
                """
        
        data = {
            'id': post_id
        }
        results = connectToMySQL(cls.DB).query_db(query,data)
        return results