from fastapi import APIRouter, status,Depends
from fastapi_jwt_auth import AuthJWT
from model import User,Order
from schemas import OrderModel, OrderStatusModel
from fastapi.exceptions import HTTPException
from database import Session, engine
from fastapi.encoders import jsonable_encoder
from pydantic import  parse_obj_as

session=Session(bind=engine)
order_router = APIRouter(
    prefix="/order",
    tags=["order"],
)



# create an order
@order_router.post('/order',status_code=status.HTTP_201_CREATED)
async def CreateOrder(order:OrderModel, Authorize : AuthJWT= Depends()):
    """
        ## Create a new Order
        This endpoint allows you to create a new order, and requires
        ```
        - pizza_size : int
        - quantity: str
        ```

    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail= "Invalid Token")
    
    current_user= Authorize.get_jwt_subject()
    user= session.query(User).filter(User.username==current_user).first()

    new_order= Order(
        pizza_size=order.pizza_size,
        quantity= order.quantity
    )
    new_order.user=user

    session.add(new_order)
    session.commit()
    response ={
        "pizza_size" : new_order.pizza_size,
        "quantity": new_order.quantity,
        "user_id": new_order.user_id,
        "order_status": new_order.order_status,
        "is_available" : new_order.is_available
    }
  
  
    return jsonable_encoder(response)

# get all order
@order_router.get('/orders')
async def list_all_orders(Authorize : AuthJWT= Depends()):
    """
        ## List all Order
        This endpoint list all orders. It can be done by a superuser or a staff

    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail= "Invalid Token")
    current_user= Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username== current_user).first()
    if user.is_staff:
        orders= session.query(Order).all()
        return jsonable_encoder(orders)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail= "You are not a Staff")

# get an order by id
@order_router.get('/order/{id}')
async def get_order_by_id(id:int,Authorize: AuthJWT=Depends()):
    """
        ## Get an Order by id
        This endpoint allows you to Get an order by id. This can only be done by a superuser and requires
        ```
        order_id : int
        ```
    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid Token")
    current_user= Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username==current_user).first()
    if user.is_staff:
        order = session.query(Order).filter(Order.id==id).first()
        return jsonable_encoder(order)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail= "User not allowed because user does not have admin privilegde.")


# get current user order
@order_router.get('/user/orders')
async def GetUserOrder(Authorize: AuthJWT=Depends()):
    """
        ## Get current user order
        This endpoint allows you to get current  logged in user's orders

    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid Token")
    user = Authorize.get_jwt_subject()
    current_user= session.query(User).filter(User.username==user).first()
    return jsonable_encoder(current_user.orders )

@order_router.get('/user/order/{id}')
async def get_specific_order(id: int, Authorize : AuthJWT=Depends()):
    """
        ## Get user specific order
        This endpoint allows you to get a user specific order, and requires
        ```   
        -order_id : id
        ```

    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail= 'Invalid Token')
    logged=Authorize.get_jwt_subject()
    current_user= session.query(User).filter(User.username==logged).first()
    order = current_user.orders
    for o in order:
        if o.id == id:
            return jsonable_encoder(o)
    raise  HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                         detail= "No order with such id")

#update order
@order_router.put('/order/update/{order_id}') #response_model=OrderModel)
async def update_an_order(order_id:int, orders:OrderModel,Authorize: AuthJWT=Depends()):
    """
        ## Update an order
        This endpoint allows you to update an order and the params can be any of 
        ```
        - pizza_size : int
        - quantity: str
        ```
    """
    try:
        Authorize.jwt_required()
    except Exception as e :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail= "invalid token")
    order_to_update = session.query(Order).filter(Order.id ==order_id).first()
    print(order_to_update )
    order_to_update.quantity = orders.quantity
    order_to_update.pizza_size= orders.pizza_size
    session.commit()
    
    response= {
            "order_status": order_to_update.order_status,
            "pizza_size": order_to_update.pizza_size,
            "is_available": order_to_update.is_available,
            "quantity": order_to_update.quantity,
        }

    return jsonable_encoder(response)


@order_router.patch('/order/status/{order_id}')
async def update_order_status(order_id:int, order_status:OrderStatusModel, Authorize: AuthJWT=Depends()):
    """
        ## update the status of an order
        This endpoint allows you to update the status of an order and can be done by a superuser. It requires
        ``` order_id : int ```
        
    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail = "invalid token")
    username = Authorize.get_jwt_subject() #for staff
    current_user = session.query(User).filter(User.username == username).first()
    if current_user.is_staff:
        order_to_update = session.query(Order).filter(Order.id == order_id).first()

        order_to_update.order_status = order_status.order_status 

        session.commit()
        response= {
            "order_status": order_to_update.order_status,
            "is_available": order_to_update.is_available,
            "quantity": order_to_update.quantity,
        }

        return jsonable_encoder(response)
    

@order_router.delete('/order/delete/{order_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id:int, Authorize: AuthJWT=Depends()):
    """
        ## Delete an Order
        This endpoint allows you to delete an order and requires
        ``` order_id : int ```

    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail = "invalid token")
    order_to_delete = session.query(Order).filter(Order.id == order_id).first()
    session.delete(order_to_delete)
    session.commit()
    return {"message": "order deleted successfully"}