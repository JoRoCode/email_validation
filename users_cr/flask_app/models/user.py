from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = 'users_cr'
    def __init__( self , data ) -> None:
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
            
    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        # print("These are the results", results)
        for user in results:
            users.append(cls(user))
        return users
    
    @classmethod
    def create_user(cls,data):
        query = """INSERT INTO users (first_name, last_name, email, created_at, updated_at)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, NOW(), NOW());"""
        return connectToMySQL('users_cr').query_db(query, data)
    
    @classmethod
    def show_user(cls, user_id):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        data = {'id': user_id}
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])
    
    
    @classmethod
    def edit_user(cls, id):
        query = """
        UPDATE users
        SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, created_at = NOW(), updated_at = NOW()
        WHERE id = %(id)s;
        """
        return connectToMySQL('users_cr').query_db(query, id)
    
    @classmethod
    def delete(cls, user_id):
        query = "DELETE FROM users WHERE id = %(id)s;"
        data = {"id": user_id}
        return connectToMySQL(cls.db).query_db(query, data)
    
    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) < 1:
            flash("First name is required.")
            is_valid = False
        if len(user['last_name']) < 1:
            flash("Last name is required.")
            is_valid = False
        if len(user['email']) < 1:
            flash("Email is required.")
            is_valid = False
            return is_valid
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address")
            is_valid = False
        return is_valid
        