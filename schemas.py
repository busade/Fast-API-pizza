from pydantic  import BaseModel
from typing import Optional

class SignUpModel(BaseModel):
    id: Optional[int]
    username : str 
    email : str
    password: str
    is_staff :Optional[bool]
    is_active : Optional[bool]


    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                'username': 'John',
                "email": "john@mail.com",
                'password': '1234',
                'is_staff': False,
                'is_active': True,
                }
        }
# for jwt token
class Settings(BaseModel):
    authjwt_algorithm: str = "HS256"
    authjwt_secret_key: str = '387d278964369e3cfe694f7dc8cecfdb93f20094ddf392674756e0a8812cfb70'


class LoginModel(BaseModel):
    username: str
    password: str

class OrderModel(BaseModel):
    id:Optional[int]
    order_status:Optional[str]='PENDING'
    quantity : int
    pizza_size : Optional[str]='SMALL'
    user_id : Optional[int]
    is_available: Optional[bool]=True


    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                'order_status': 'PENDING',
                "quantity": "1",
                'pizza_size': 'LARGE',
                'is_available': True,
                }
        }
class OrderStatusModel(BaseModel):
    order_status: Optional[str]='PENDING'

    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                'order_status': 'PENDING',
                }
        }