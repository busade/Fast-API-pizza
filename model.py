from database import Base
from sqlalchemy import Column, Integer, Text,String, Boolean,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType


class User(Base):
    __tablename__ = 'user'
    id= Column(Integer, primary_key=True)
    username= Column(String(50), unique=True, nullable=False)
    email= Column(String(50),unique=True, nullable=False)
    password= Column(Text, nullable=False)
    is_staff= Column(Boolean, default=False)
    is_active= Column(Boolean, default=False)
    orders= relationship('Order', back_populates='user')
    def __repr__(self):
        return f'User {self.username}'
    

class Order(Base):

    ORDER_STATUSES = (
        ('PENDING','pending'),
        ('IN-TRANSIT','in-transit'),
        ('DELIVERED','delivered'),

    )
    PIZZA_SIZES = (
        ('SMALL','small'),
        ('MEDIUM','medium'),
        ('LARGE', 'large'),
        ('XTRA-LARGE', 'xtra-large')

    )
    __tablename__ = 'orders'
    id= Column(Integer, primary_key=True)
    order_status= Column(ChoiceType(choices=ORDER_STATUSES), default= 'PENDING')
    quantity= Column(Integer, nullable=False)
    pizza_size= Column(ChoiceType(choices=PIZZA_SIZES), default='SMALL')
    is_available= Column(Boolean, default=True)
    user_id= Column(Integer, ForeignKey('user.id'))
    user= relationship('User', back_populates='orders')

    def __repr__(self):
        return f'Order {self.id}'
