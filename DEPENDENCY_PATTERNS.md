# FastAPI Dependency Injection Patterns

This document explains different approaches to implementing dependency injection in FastAPI, specifically for the `UserService` in our system Management API.

---

## Pattern 1: Global Instance (Simple)

### Implementation
```python
from system_service import UserService

# Create a global instance
user_service = UserService()

def get_user_service():
    """Return the global user service instance"""
    return user_service
```

### Pros ✅
- Simple and straightforward
- Easy to understand for beginners
- Minimal boilerplate code

### Cons ❌
- Hard to test (can't easily mock or replace)
- No lifecycle management (startup/shutdown)
- Global state can lead to hidden dependencies
- Not ideal for resources that need initialization/cleanup

### Use Case
Good for: Small scripts, prototypes, learning projects

---

## Pattern 2: LRU Cache Singleton

### Implementation
```python
from functools import lru_cache
from system_service import UserService

@lru_cache(maxsize=None)
def get_user_service():
    """Create and cache a single UserService instance"""
    return UserService()
```

### Pros ✅
- Ensures only one instance is created (singleton pattern)
- Thread-safe
- Automatic caching by Python's functools
- Still relatively simple

### Cons ❌
- Cannot access `app.state` or application context
- No control over initialization timing
- Difficult to clear/reset for testing
- No shutdown hook for cleanup
- Cache persists across test runs (can cause issues)

### Use Case
Good for: Services that don't need app context, stateless utilities

---

## Pattern 3: App State with Lifespan (Recommended) ⭐

### Implementation

**system_dependencies.py:**
```python
from system_service import UserService
from fastapi import Request

def get_user_service(request: Request) -> UserService:
    """Get user service from app state"""
    return request.app.state.user_service
```

**system.py:**
```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from system_service import UserService

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize resources
    app.state.user_service = UserService(csv_path="users.csv")
    print("✓ User service initialized")
    
    yield  # Application runs here
    
    # Shutdown: Cleanup resources
    print("✓ Shutting down user service")

sapp = FastAPI(lifespan=lifespan)
```

### Pros ✅
- **Full lifecycle control** (startup/shutdown hooks)
- **Access to app configuration** via `request.app.state`
- **Easy to test** (can override dependencies)
- **Follows FastAPI best practices**
- **Scalable** (works with DB connections, connection pools, etc.)
- **Clean separation** of initialization and usage
- **Environment-aware** (can configure differently for dev/prod)

### Cons ❌
- Slightly more boilerplate
- Requires understanding of context managers
- Need to remember to initialize in lifespan

### Use Case
Good for: **Production applications**, services with initialization/cleanup, database connections, cache clients, external API clients

---

## Comparison Table

| Feature | Global Instance | LRU Cache | App State (Recommended) |
|---------|----------------|-----------|------------------------|
| Simplicity | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| Testability | ❌ | ⚠️ | ✅ |
| Lifecycle Control | ❌ | ❌ | ✅ |
| App Context Access | ❌ | ❌ | ✅ |
| Thread Safety | ⚠️ | ✅ | ✅ |
| Scalability | ❌ | ⚠️ | ✅ |
| Production Ready | ❌ | ⚠️ | ✅ |

---

## Real-World Example: Database Connection

The **App State pattern** shines when working with databases:

```python
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create connection pool
    engine = create_async_engine("postgresql+asyncpg://user:pass@localhost/db")
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    app.state.db_engine = engine
    app.state.session_maker = async_session
    
    print("✓ Database connected")
    
    yield
    
    # Shutdown: Close all connections
    await engine.dispose()
    print("✓ Database disconnected")

async def get_db_session(request: Request):
    """Dependency to get database session"""
    async with request.app.state.session_maker() as session:
        yield session
```

---

## When to Use Each Pattern

### Use **Global Instance** when:
- Building a quick prototype
- Learning FastAPI basics
- Service has no initialization/cleanup needs
- Not planning to write tests

### Use **LRU Cache** when:
- Need a singleton pattern
- Service is stateless
- Don't need startup/shutdown hooks
- Not accessing app configuration

### Use **App State (Recommended)** when:
- Building production applications
- Need initialization/cleanup (DB connections, file handles)
- Want to write tests with mocked dependencies
- Service needs app configuration
- Planning to scale the application
- Working with external resources (databases, caches, APIs)

---

## Migration Path

If you're currently using Pattern 1 or 2, here's how to migrate to Pattern 3:

### Step 1: Update Dependencies
```python
# Before
def get_user_service():
    return user_service

# After
def get_user_service(request: Request) -> UserService:
    return request.app.state.user_service
```

### Step 2: Add Lifespan
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize your service
    app.state.user_service = UserService(csv_path="users.csv")
    yield
    # Cleanup if needed

sapp = FastAPI(lifespan=lifespan)
```

### Step 3: Remove Global Instance
```python
# Remove this line
# user_service = UserService()
```

---

## Testing with App State Pattern

The App State pattern makes testing much easier:

```python
from fastapi.testclient import TestClient
from unittest.mock import Mock

def test_get_users():
    # Create mock service
    mock_service = Mock(spec=UserService)
    mock_service.get_all_users.return_value = [...]
    
    # Override dependency
    def override_get_user_service():
        return mock_service
    
    sapp.dependency_overrides[get_user_service] = override_get_user_service
    
    # Test endpoint
    client = TestClient(sapp)
    response = client.get("/users")
    
    assert response.status_code == 200
    mock_service.get_all_users.assert_called_once()
```

---

## Conclusion

For the system Management API, we use **Pattern 3 (App State with Lifespan)** because:
1. It provides full control over the service lifecycle
2. Makes the code testable and maintainable
3. Follows FastAPI's recommended practices
4. Scales well as the application grows
5. Makes it easy to add new resources (databases, caches, etc.)

This pattern is the foundation for building robust, production-ready FastAPI applications.

---

## Further Reading

- [FastAPI Dependency Injection](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [FastAPI Lifespan Events](https://fastapi.tiangolo.com/advanced/events/)
- [Dependency Injection Principles](https://en.wikipedia.org/wiki/Dependency_injection)