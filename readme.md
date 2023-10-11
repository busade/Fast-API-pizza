# Pizza Delivery with Fast API
<h3>This is a Pizza Order Delivery API built  with Fast API framework.It takes an order from a registered user and allows the user track the status of their order.</h3>

## Getting Started
To get started with this project,follow the following steps:

-clone the repository
-go to terminal and `pip install requirements.txt`

## Usage 
### To lauch the app
go to terminal and type``` uvicorn main:app```

### Create a new User
To create  a new user, make a POST Request to the route `/auth/signup `

### Log in a user
To log in a User, make GET request to the route ` /auth/login`

### Create an Order
To create an order, make POST request to the route ` /order/order`

### Get all Order
To get all order made (only accessible by a staff), make a GET request to the route ` /order/orders`

### Get a particular Order by id
To a particular order by id, make GET request to the route ` /order/order/{id}` replace id with the id of the order

### Get a user's order
This endpoint will  return all orders made a current user, make a GET request to the route ` /order/user/orders`


### Get a specific order by user
This endpoint will  return a specific order made by a user, make a GET request to the route `/order/user/order/{id}`. id should be replaced by order_id

### Update an order
This endpoint updates an order, make a PUT request to the route ` /order/order/status/{order_id}`. The paramter this will take includes quanity and pizza size, depending on which you want to update

### Update the status of an order
This endpoint updates the status of an order, make a PATCH request to the route ` /order/order/status/{order_id}`

