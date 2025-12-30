from flask_restful import Resource, reqparse
from flask import request
from api.models.user import User,roleEnum
from api.utils import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token

user_request_parser = reqparse.RequestParser()
login_request_parser = reqparse.RequestParser()


user_request_parser.add_argument("email",type=str,required=True, help="Email is required")
user_request_parser.add_argument("username", type=str, required=True, help="Username is required")
user_request_parser.add_argument("password", type=str, required=True, help="Password is required")
user_request_parser.add_argument("phone_number",type=str, required=True, help="Phone number is required")
user_request_parser.add_argument("role", type=str, required=False, help="Role number of the user")

login_request_parser.add_argument("email", required=True)
login_request_parser.add_argument("password", required = True)


class  SignUp(Resource):
    
    def post(self):
        data = user_request_parser.parse_args()
        email = data["email"]
        username = data["username"]
        password = data["password"]
        phone_number = data["phone_number"]
        role= data.get("role")

        if User.query.filter_by(email=email).first():
            print("here")
            return {"message": "Email already exists"}, 409
        if User.query.filter_by(username=username).first():
            print("Secondly")
            return {"message": "Username already exists"}, 409
        if role:
            role = role.upper()
            if role not in ['ADMIN', 'CUSTOMER']:
                return {"message": "Invalid role. Allowed values: ADMIN, CUSTOMER"},400
        password_hash = generate_password_hash(password)
        new_user = User(
            email= email,
            username=username,
            password=password_hash,
            phone_number=phone_number,
            role=role
        )
        db.session.add(new_user)
        db.session.commit()

        return{"message": "user created successfully",
               "user":{
                    "email": new_user.email, 
                    "username": new_user.username,
                    "phone_number": new_user.phone_number,
                    "role": role
               }}, 201
    

class Login(Resource):
    def post(self):
        data =login_request_parser.parse_args()

        email = data["email"]
        password= data["password"]

        user_check = User.query.filter_by(email=email).first()
        if user_check:
            if check_password_hash(user_check.password, password):
                access_token= create_access_token(identity= str(user_check.id),additional_claims= {"role":user_check.role.value})
                refresh_token= create_refresh_token(identity= str(user_check.id))

                return{
                    "message":"Login successful",
                    "access_token": access_token,
                    "refresh_token":refresh_token
                    }, 200
            else:
                return{"message":"Invalid password"}, 401
        else:
            return{"message":"Invalid email address"}, 401

