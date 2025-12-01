from fastapi import FastAPI, status, Depends, Request
from typing import List, Optional, Annotated
from fastapi.security import OAuth2PasswordRequestForm
from system_schema import UserResponse, UserEnter, UserUpdate
from system_service import UserService
from contextlib import asynccontextmanager
from system_dependencies import get_user_service
from system_utils import login as login_handler, require_roles, get_current_user
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize shared resources
    app.state.counter = 0
    app.state.user_service = UserService(csv_path="users.csv")
    print("Starting Up ...", os.getpid())
    print(f"✓ User service initialized with {app.state.user_service.get_users_count()} users")

    yield  # Application runs here

    # Shutdown: Cleanup resources
    print("Shutting Down ...")
    print(f"✓ Total requests handled: {app.state.counter}")


sapp = FastAPI(lifespan=lifespan)


@sapp.get("/")
async def root(request: Request):
    # print(vars(request))

    # print("URL:", request.url)
    # print("Base URL:", request.base_url)
    # print("Headers:", request.headers)
    # print("Query Params:", request.query_params)
    # print("Path Params:", request.path_params)
    # print("Cookies:", request.cookies)
    # print("Client:", request.client)
    # print("Method:", request.method)
    # print("Scope:", request.scope)
    # print("State:", request.state)
    # print("App:", request.app)
    # # print("Session:", getattr(request, "session", None))

    request.app.state.counter += 1
    print(f"Counter: {request.app.state.counter}")
    return {"System Message": "Hello Users!", "Counter": request.app.state.counter}

@sapp.post("/token", response_model=dict)
async def login_for_access_token(request: Request, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> dict:
    return await login_handler(request, form_data)


@sapp.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current authenticated user's information"""
    return current_user["user"]


@sapp.get("/users", response_model=List[UserResponse])
async def get_users(
        length: Optional[int] = None,
        offset: Optional[int] = None,
        user_service: UserService = Depends(get_user_service),
        current_user: dict = Depends(require_roles(["principal", "worker", "user"]))
):
    """Get all users with optional pagination - All roles can access"""
    return user_service.get_all_users(length=length, offset=offset)


@sapp.get("/users/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def find_user(
        user_id: int,
        user_service: UserService = Depends(get_user_service),
        current_user: dict = Depends(require_roles(["principal", "worker", "user"]))
):
    """Get a specific user by ID - All roles can access"""
    return user_service.get_user_by_id(user_id)


@sapp.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def add_user(
        user: UserEnter,
        user_service: UserService = Depends(get_user_service),
        current_user: dict = Depends(require_roles(["principal"]))
):
    """Create a new user - Only Principal can access"""
    return user_service.create_user(user)


@sapp.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
        user_id: int,
        user_update: UserUpdate,
        user_service: UserService = Depends(get_user_service),
        current_user: dict = Depends(require_roles(["principal", "worker"]))
):
    """Full update of a user - Principal and Worker can access"""
    return user_service.update_user(user_id, user_update, current_user["role"], int(current_user["user_id"]))


@sapp.patch("/users/{user_id}", response_model=UserResponse)
async def patch_user(
        user_id: int,
        user_patch: UserUpdate,
        user_service: UserService = Depends(get_user_service),
        current_user: dict = Depends(require_roles(["principal", "worker"]))
):
    """Partial update of a user - Principal and Worker can access"""
    return user_service.patch_user(user_id, user_patch, current_user["role"], int(current_user["user_id"]))


@sapp.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        user_id: int,
        user_service: UserService = Depends(get_user_service),
        current_user: dict = Depends(require_roles(["principal"]))
):
    """Delete a user - Only Principal can access"""
    user_service.delete_user(user_id)
    return None  # 204 No Content