from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

#Creation of the class of Post
class Thought:
    db_name='provimdb' # Our database name in the workbench
    def __init__(self,data):
        self.id = data['id'],
        self.content = data['content'],
        self.user_id = data['user_id'],
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    #Method to  query the database and 
    #get all the posts, together with the creator's id and email,
    # and the number of likes

    @classmethod
    def getAllThoughts(cls):
        query= 'SELECT thoughts.id, content, COUNT(likes.id) as likesNr, users.id as creator_id, email, name FROM thoughts LEFT JOIN users on thoughts.user_id = users.id LEFT JOIN likes on likes.thought_id = thoughts.id GROUP BY thoughts.id;'
        results =  connectToMySQL(cls.db_name).query_db(query)
        thoughts= []
        for row in results:
            thoughts.append(row)
        return thoughts
        
    @classmethod
    def create_thought(cls,data):
        query = 'INSERT INTO thoughts (content, user_id) VALUES ( %(content)s, %(user_id)s );'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_thought_by_id(cls, data):
        query= 'SELECT * FROM thoughts WHERE thoughts.id = %(thought_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results[0]


    @classmethod
    def get_user_thoughts(cls, data):
        query= 'SELECT * FROM users LEFT JOIN thoughts on thoughts.user_id = users.id WHERE users.id = %(user_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        thoughts = []
        for row in results:
            thoughts.append(row)
        return thoughts

    @classmethod
    def addLike(cls, data):
        query= 'INSERT INTO likes (thought_id, user_id) VALUES ( %(thought_id)s, %(user_id)s );'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def removeLike(cls, data):
        query= 'DELETE FROM likes WHERE thought_id = %(thought_id)s and user_id = %(user_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def destroyThought(cls, data):
        query= 'DELETE FROM thoughts WHERE thoughts.id = %(thought_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)
    @classmethod
    def deleteAllLikes(cls, data):
        query= 'DELETE FROM likes WHERE likes.thought_id = %(thought_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @staticmethod
    def validate_thought(thought):
        is_valid = True
        if len(thought['content']) < 5:
            flash("Thought content must be at least 5 characters.", 'content')
            is_valid = False
        return is_valid