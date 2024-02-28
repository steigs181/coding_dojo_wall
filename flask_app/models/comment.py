from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

class Comment():

    DB = "coding_dojo_wall_schema"

    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.user_id = data['user_id']
        self.post_id = data['post_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.owner = None

    @classmethod
    def save_comment(cls, data):
        query = """
                INSERT INTO comments (content, user_id, post_id)
                VALUES (%(content)s, %(user_id)s, %(post_id)s)
                """
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results
    
    @classmethod
    def get_comment_owner_by_id(cls, comment_id):
        query = """
                SELECT * FROM users WHERE id = %(id)s
            """
        data = {
            'id': comment_id
        }
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results