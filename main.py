from fastapi import FastAPI
from auth_routes import auth_router
from order_routes import order_router
from fastapi_jwt_auth import AuthJWT
from schemas import Settings
import inspect, re
from fastapi.routing import APIRoute
from fastapi.openapi.utils import get_openapi

app = FastAPI()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Pizza API",
        version="1.0.0",
        description="An api for pizza ordering",
        routes=app.routes,

    )
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Enter: **'Bearer &lt;JWT&gt;'**, where JWT is the token"
        }
    }
#   get all routes with jwt_required()
    api_routes = [route for route in app.routes if isinstance(route, APIRoute) and route.dependant.dependencies]
    for route in api_routes:
        path = getattr(route, "path")
        endpoint = getattr(route, "endpoint")
        methods = [method.lower() for method in getattr(route, "methods")]

        for method in methods:
            # access_token
            if(
                re.search("access_token", inspect.getsource(endpoint)) or
                re.search("fresh_jwt_required", inspect.getsource(endpoint)) or
                re.search('jwt_required', inspect.getsource(endpoint)) 
            ):
                openapi_schema["paths"][path][method]["security"] = [
                    {
                        "bearerAuth": []
                    }
                    ]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi



# to create an instance of setting class in schemas.py
@AuthJWT.load_config
def get_config():
    return Settings()
app.include_router(auth_router)
app.include_router(order_router)