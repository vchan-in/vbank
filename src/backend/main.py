import os

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from cmd.api.main import router as customer_router
from cmd.api.admin import router as admin_router

from handlers.gql import graphql_app


FVB_BACKEND_BASEURL = os.getenv("FVB_BACKEND_BASEURL", "http://127.0.0.1")
FVB_BACKEND_PORT = os.getenv("FVB_BACKEND_PORT", "8000")
FVB_BACKEND_BASEURLPORT = f"{FVB_BACKEND_BASEURL}:{FVB_BACKEND_PORT}"

methods = ["GET", "POST", "DELETE", "OPTIONS", "PUT", "PATCH"]

app = FastAPI(
        redirect_slashes=False,
        title="FVB API",
        description="A vulnerable bank",
        version="24.09",
        servers=[
            {"url": "http://localhost:8000", "description": "Development environment"},
            {"url": FVB_BACKEND_BASEURLPORT , "description": "Production environment"},
        ],
    )

origins = ['http://localhost:8080', 'http://127.0.0.1:8080']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}

# REST routes
app.include_router(customer_router, prefix="/api/v1", tags=["customer"])   # Include the customer router
app.include_router(admin_router, prefix="/api/v1/admin", tags=["admin"])   # Include the admin router

# GraphQL routes
app.include_router(graphql_app, prefix="/graphql")
app.add_websocket_route("/graphql", graphql_app)
