from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, db_data):
        self.id = db_data["id"]
        self.first_name = db_data["first_name"]
        self.last_name = db_data["last_name"]
        self.email = db_data["email"]
        self.password = db_data["password"]
        self.points = db_data["points"]
        self.created_at = db_data["created_at"]
        self.updated_at = db_data["updated_at"]
    
    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user["first_name"]) < 2:
            flash("First Name must be at least 2 characters")
            is_valid = False
        if len(user["last_name"]) < 2:
            flash("Last Name must be at least 2 characters")
            is_valid = False
        if not EMAIL_REGEX.match(user["email"]): 
            flash("Invalid email address!")
            is_valid = False
        if not user["password"] == user["confirm_password"]:
            is_valid = False
        return is_valid
    
    @classmethod
    def save(cls, data):
        query =  "INSERT INTO users (first_name, last_name, email, password, points, created_at, updated_at) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s, %(points)s, NOW(), NOW() );"
        return connectToMySQL('math_master').query_db( query, data)
    
    @classmethod
    def get_by_email(cls,data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        result = connectToMySQL('math_master').query_db(query,data)
        
        if len(result) < 1:
            return False
        return cls( result[0])
    
    @classmethod
    def get_by_id(cls,data):
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        result = connectToMySQL('math_master').query_db(query,data)
        
        return cls(result[0])
    @classmethod
    def getAll(cls):   
        query = 'SELECT * FROM users;'
        results = connectToMySQL('math_master').query_db(query)
        users = []
        
        for user in results:
            users.append( cls(user) )
        return users
    