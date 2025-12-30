from flask import Flask
from flask_restful import Api
from api.utils import db
from api.config.config import config_dict
from api.controller.auth import SignUp, Login
from api.controller.order import create_order, admin_panel, user_order, project
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate


def create_app(config = config_dict["dev"]):
    app =Flask(__name__)
    app.config.from_object(config)
    JWTManager(app)
    api = Api(app)
    db.init_app(app)
    Migrate(app,db)



    api.add_resource(SignUp, "/signup")
    api.add_resource(Login, "/login")
    api.add_resource(create_order,"/order")
    api.add_resource(admin_panel, "/admin/orders")
    api.add_resource(user_order,"/order/user/<int:order_id>")
    api.add_resource(project,"/admin/order/user/<int:user_id>/order/<int:order_id>")

    
    with app.app_context():
        db.create_all()
    return app