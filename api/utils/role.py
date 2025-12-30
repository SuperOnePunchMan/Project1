from flask_jwt_extended import get_jwt, verify_jwt_in_request
from api.models.user import User
from functools import wraps
from flask import request



def role_required(*roles):
    def wrapper(a):
        @wraps(a)
        def helper(*args, **kwargs):
            verify_jwt_in_request()
            user= get_jwt()
            user_role= user.get("role", "")

            if user_role not in roles:
                return{"message":"You are not authorized to access this resouce"}, 401
            return a(*args,**kwargs)
        return helper
    return wrapper
