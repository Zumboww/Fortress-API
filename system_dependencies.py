from system_service import UserService
from fastapi import Request

# user_service = UserService()
# def get_user_service():
#     return user_service

# from functools import lru_cache
# @lru_cache(maxsize=None)
# def get_user_service():
#     return UserService()

def get_user_service(request: Request) -> UserService:
    """Get user service from app state"""
    return request.app.state.user_service