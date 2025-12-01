from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from typing import Union, Any, Annotated, List
from jose import jwt, JWTError
from fastapi import Depends, Request
import os
from system_exceptions import InvalidCredentialsException, ForbiddenException

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "Qwqwqw121212")   # should be kept secret
JWT_REFRESH_SECRET_KEY = os.environ.get("JWT_REFRESH_SECRET_KEY", "Qwqwqw121212Refresh")    # should be kept secret
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def get_password_verify(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

def create_access_token(subject: Union[str, Any], role: str, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.now(timezone.utc) + expires_delta
    else:
        expires_delta = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject), "role": role}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt

def create_refresh_token(subject: Union[str, Any], role: str, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.now(timezone.utc) + expires_delta
    else:
        expires_delta = datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject), "role": role}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt

async def get_current_user(request: Request, token: str = Depends(oauth2_schema)) -> dict:
    """Get current user from access token"""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        role = payload.get("role")
        
        if user_id is None or role is None:
            raise InvalidCredentialsException()
        
        # Get full user info from service
        user_service = request.app.state.user_service
        user = user_service.get_user_by_id(int(user_id))
        
        return {"user_id": user_id, "role": role, "user": user}
    except JWTError:
        raise InvalidCredentialsException()

def require_roles(allowed_roles: List[str]):
    """Dependency to check if user has required role"""
    async def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user["role"] not in allowed_roles:
            raise ForbiddenException(
                f"Access denied. Required roles: {', '.join(allowed_roles)}"
            )
        return current_user
    return role_checker

async def login(request: Request, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> dict:
    user_service = request.app.state.user_service
    user = await user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise InvalidCredentialsException()
    
    access_token = create_access_token(user.user_id, user.role)
    refresh_token = create_refresh_token(user.user_id, user.role)
    return {
        "access_token": access_token, 
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "role": user.role
    }