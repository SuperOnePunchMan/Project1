from flask_jwt_extended import get_jwt_identity
from flask_restful import Resource, reqparse
from flask import jsonify, request

from api.models.orders import Order, OrderStatus
from api.utils.menu import Menu
from api.utils import db
from api.utils.role import role_required
from api.models.user import roleEnum
import requests


order_request = reqparse.RequestParser()

order_request.add_argument("Size", required =True)
order_request.add_argument("Quantity", required= True)
order_request.add_argument("Topping")
order_request.add_argument("Address", required= True)
order_request.add_argument("pizza_type",required=True)

class create_order(Resource):
    @role_required(roleEnum.CUSTOMER.value)
    def post(self):
        try:
            data = order_request.parse_args()
            size = (data["Size"]).lower()
            quantity= int(data.get("Quantity"))
            topping = int(data.get("Topping",0))
            address = data["Address"]
            pizza_type = data["pizza_type"]

            if size.lower() not in Menu:
                return{"Message":"Please Provide A Valid Size From The Menu"}
            if pizza_type not in Menu[size]:
                return {"Message":"Please Provide A Valid Pizza Type"}
            if topping < 0:
                return{"Message": "Provide A Value Greater Than Zero"}
        
            base_price= Menu[size][pizza_type]
            topping_price=Menu[size]["toppings"] 
            total_price= (base_price +topping_price) * quantity
            tax= total_price * 0.1
            Amount = total_price+ tax
        
            user =get_jwt_identity()

            new_order =Order(
                address="address",
                user_id=user,
                size =size,
                quantity= quantity,
                amount=Amount,
                toppings= topping
            )
            db.session.add(new_order)
            db.session.commit()
            return ({
                "status":"success",
                "data": new_order.to_dict(),
                "Status_code": 201
            }),
        except Exception as e:
            return{
            "status":"failed",
            "message": str(e)
        }
    


    @role_required(roleEnum.CUSTOMER.value)
    def get(self):
        """This endpoint returns all orders of a user"""
        try:
            user=get_jwt_identity()
            orders= Order.query.filter_by(user_id=user).all()
            return({
                "status":"success",
                "data": [order.to_dict() for order in orders],
                "status_code":200
            })
        except Exception as e:
            return{
            "status": "failed",
            "message": str(e)
        }
        
class user_order(Resource):
    @role_required(roleEnum.CUSTOMER.value)
    def get(self, order_id):
        """This endpoint gets a single order"""
        try:
            user=get_jwt_identity()
            order =Order.query.filter_by(user_id=user, id=order_id).first()
            
            if not order:
                return {"message": "Order not found"},404

            return {
                "status": "success",
                "data": order.to_dict()}, 200
        except Exception as e:
            return {"message": str(e)}



class admin_panel(Resource):

    @role_required(roleEnum.ADMIN.value)
    def get(self):
        """ This endpoints all orders accesable only to admins"""
        try:

            orders= Order.query.all()

            return {
                "status": "success",
                "data": [order.to_dict() for order in orders],
                "status_code": 200
            }
        except Exception as e:
            return{
            "status":"failed",
            "message": str(e)
        }


class project(Resource):

    @role_required(roleEnum.ADMIN.value)
    def get(self,user_id,order_id):
        """This endpoint gets a singular order by a user"""
        try:
            order= Order.query.filter_by (user_id=user_id, id=order_id).first()
            if not order:
                return{"message": "Order not found"},404
            return {
                "status": "success",
                "data": order.to_dict(),
            }, 200
        except Exception as e:
            return{
            "status":"failed",
            "message": str(e)
        }
    
    @role_required(roleEnum.ADMIN.value)
    def patch(self,user_id,order_id):
        """This endpoint updates order status by admin"""
        try:
            order=Order.query.filter_by(id=order_id, user_id=user_id).first()
            if not order:
                return{"message": "Order not found"},404
            data = request.get_json()
            new_status = data.get("order_status").lower()
            if new_status not in [status.value for status in OrderStatus]:
                return {"status": "failed",
                    "message": "Invalid order status"},400
            order.order_status = new_status
            db.session.commit()
            return{
                "status": "success",
                "data": order.to_dict(),
            },200
        except Exception as e:
            return{
            "status":"failed",
            "message": str(e)
        }
    
        


    @role_required(roleEnum.ADMIN.value)
    def delete(self,user_id,order_id):
        """This endpoint deletes an order by id"""
        try:
            order_to_delete = Order.query.filter_by(id=order_id, user_id=user_id).first()
            if not order_to_delete:
                return{
                    "status": "failed",
                    "message": "Order not found"
                }, 404
            db.session.delete(order_to_delete)
            db.session.commit()
            return {
                "status":"success",
                "message": "Order deleted  successfully"                    
            },200
        except Exception as e:
            return{
            "status":"failed",
            "message": str(e)
        }