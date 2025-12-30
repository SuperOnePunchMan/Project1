from api.utils import db
import enum

class roleEnum(enum.Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key= True)
    username= db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(70),unique= True, nullable= False)
    password = db.Column(db.String(70), nullable= False)
    phone_number= db.Column(db.String(15), nullable= False)
    is_active = db.Column(db.Boolean, default= True)
    role = db.Column(db.Enum(roleEnum), default=roleEnum.CUSTOMER)


    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email})"
    
