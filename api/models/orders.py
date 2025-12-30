from api.utils import db
from enum import Enum

class OrderStatus(Enum):
    PENDING= "pending"
    In_Transit = "in_transit"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class Size(Enum):
    SMALL= "small"
    MEDIUM= "medium"
    LARGE= "large"
    PERSONAL= "personal"



class Order(db.Model):
    __tablename__="orders"
    id= db.Column(db.Integer,primary_key=True)
    user_id =  db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    size = db.Column(db.String, default=Size.MEDIUM.value)
    order_status= db.Column(db.String, default=OrderStatus.PENDING.value)
    quantity = db.Column(db.Integer,default=1)
    amount = db.Column(db.Float, nullable = False)
    address= db.Column(db.String, nullable = False)
    toppings= db.Column(db.Integer, )


    customer= db.relationship("User", backref=db.backref("orders", ))
    def __repr__(self):
        return f"Order <self.id>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "size": self.size,
            "order_status": self.order_status,
            "quantity": self.quantity,
            "amount": self.amount,
            "topping":self.toppings,
            "address": self.address
        }
