# Contributing to Fortress API 🤝

First off, thank you for considering contributing to Fortress API! It's people like you that make this project such a great tool for the community.

## 📋 Table of Contents

- [Code of Conduct](#-code-of-conduct)
- [How Can I Contribute?](#-how-can-i-contribute)
- [Development Setup](#-development-setup)
- [Coding Standards](#-coding-standards)
- [Commit Guidelines](#-commit-guidelines)
- [Pull Request Process](#-pull-request-process)
- [Reporting Bugs](#-reporting-bugs)
- [Suggesting Features](#-suggesting-features)

---

## 📜 Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to [memoryaz98@gmail.com].

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of:
- Age, body size, disability, ethnicity
- Gender identity and expression
- Level of experience, education
- Nationality, personal appearance, race, religion
- Sexual identity and orientation

### Our Standards

**Positive behavior includes:**
- ✅ Using welcoming and inclusive language
- ✅ Being respectful of differing viewpoints
- ✅ Gracefully accepting constructive criticism
- ✅ Focusing on what is best for the community
- ✅ Showing empathy towards others

**Unacceptable behavior includes:**
- ❌ Trolling, insulting/derogatory comments, personal attacks
- ❌ Public or private harassment
- ❌ Publishing others' private information
- ❌ Other conduct which could reasonably be considered inappropriate

---

## 🎯 How Can I Contribute?

### 🐛 Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include as many details as possible:

**Bug Report Template:**

```markdown
**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Send request to '...'
2. With payload '...'
3. See error

**Expected behavior**
What you expected to happen.

**Actual behavior**
What actually happened.

**Environment:**
- OS: [e.g., Ubuntu 24.04, Windows 11]
- Python Version: [e.g., 3.14.0]
- FastAPI Version: [e.g., 0.123.0]

**Additional context**
Add any other context, logs, or screenshots.
```

### 💡 Suggesting Features

Feature suggestions are welcome! Please provide:

**Feature Request Template:**

```markdown
**Is your feature request related to a problem?**
A clear description of the problem. Ex. I'm frustrated when [...]

**Describe the solution you'd like**
A clear description of what you want to happen.

**Describe alternatives you've considered**
Any alternative solutions or features you've considered.

**Additional context**
Add any other context, mockups, or examples.
```

### 🔧 Contributing Code

We actively welcome your pull requests! Here's how:

1. Fork the repo and create your branch from `main`
2. Make your changes
3. Add tests if you've added functionality
4. Ensure tests pass
5. Update documentation
6. Submit your pull request!

---

## 🚀 Development Setup

### Prerequisites

- Python 3.8+
- Git
- A code editor (VS Code, PyCharm, etc.)

### Step-by-Step Setup

```bash
# 1. Fork and clone the repository
git clone https://github.com/Zumboww/Fortress-API.git
cd fortress-api

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install development dependencies
pip install -r requirements-dev.txt

# 5. Create a feature branch
git checkout -b feature/your-feature-name

# 6. Make your changes and test
uvicorn system:sapp --reload

# 7. Run tests (when available)
pytest

# 8. Commit and push
git add .
git commit -m "feat: add your feature"
git push origin feature/your-feature-name
```

### Project Structure

```
fortress-api/
├── system.py              # Main FastAPI application
├── system_service.py      # Business logic
├── system_scheme.py       # Data models
├── system_utils.py        # Utilities (JWT, hashing)
├── system_exceptions.py   # Custom exceptions
├── system_dependencies.py # Dependency injection
├── users.csv             # Data storage
└── tests/                # Test files (add yours here!)
```

---

## 📝 Coding Standards

### Python Style Guide

We follow **PEP 8** with some modifications:

#### General Rules
- ✅ Use 4 spaces for indentation (not tabs)
- ✅ Maximum line length: 100 characters
- ✅ Use descriptive variable names
- ✅ Add docstrings to all functions/classes
- ✅ Type hints are required for function signatures

#### Examples

**Good:**
```python
async def get_user_by_id(user_id: int) -> UserID:
    """
    Retrieve a user by their unique identifier.
    
    Args:
        user_id: The unique identifier of the user
        
    Returns:
        UserID: The user object with all details
        
    Raises:
        UserNotFoundException: If user doesn't exist
    """
    user = next((u for u in self.users if u.user_id == user_id), None)
    if not user:
        raise UserNotFoundException()
    return user
```

**Bad:**
```python
def get_user(id):  # No type hints, no docstring
    u = next((x for x in self.users if x.user_id == id), None)  # Unclear variable names
    if not u: raise UserNotFoundException()  # Multiple statements on one line
    return u
```

### Code Organization

#### Imports
```python
# 1. Standard library imports
from typing import List, Optional
from datetime import datetime

# 2. Third-party imports
from fastapi import FastAPI, Depends
from pydantic import BaseModel

# 3. Local application imports
from system_scheme import User, UserID
from system_exceptions import UserNotFoundException
```

#### Function Order
1. Public methods first
2. Private methods last (prefixed with `_`)
3. Group related methods together

### Security Best Practices

When contributing, ensure:

- ✅ Never log passwords or sensitive data
- ✅ Always hash passwords before storing
- ✅ Validate all user inputs
- ✅ Use parameterized queries (prevent injection)
- ✅ Add appropriate error handling
- ✅ Follow the principle of least privilege

---

## 📦 Commit Guidelines

We use **Conventional Commits** for clear and structured commit history.

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Code style changes (formatting, missing semicolons, etc.)
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `perf`: Performance improvements
- `test`: Adding missing tests
- `chore`: Changes to build process or auxiliary tools

### Examples

```bash
# Feature
feat(auth): add refresh token rotation

# Bug fix
fix(users): prevent principal deletion

# Documentation
docs(readme): update installation instructions

# Refactor
refactor(service): simplify user validation logic

# Performance
perf(csv): optimize data loading with polars

# Style
style(utils): format code according to PEP 8
```

### Detailed Example

```
feat(auth): implement refresh token rotation

- Add new endpoint for token refresh
- Invalidate old refresh tokens after use
- Update JWT utility functions
- Add tests for token rotation

Closes #123
```

---

## 🔄 Pull Request Process

### Before Submitting

- [ ] Code follows the project's style guidelines
- [ ] Self-review of your own code completed
- [ ] Comments added to hard-to-understand areas
- [ ] Documentation updated (if needed)
- [ ] No new warnings generated
- [ ] Tests added (if applicable)
- [ ] All tests pass

### PR Template

When creating a PR, use this template:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that causes existing functionality to change)
- [ ] Documentation update

## How Has This Been Tested?
Describe the tests you ran and how to reproduce

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code where needed
- [ ] I have updated the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix/feature works
- [ ] New and existing tests pass locally

## Screenshots (if applicable)
Add screenshots here

## Related Issues
Closes #(issue number)
```

### Review Process

1. **Submit PR**: Create your pull request with a clear description
2. **Automated Checks**: CI/CD runs tests (when configured)
3. **Code Review**: Maintainers review your code
4. **Address Feedback**: Make requested changes
5. **Approval**: Once approved, maintainers will merge
6. **Celebration**: You're now a contributor! 🎉

---

## 🧪 Testing Guidelines

### Writing Tests

We use `pytest` for testing. Place test files in the `tests/` directory.

**Test File Structure:**
```
tests/
├── test_auth.py
├── test_users.py
├── test_service.py
└── conftest.py  # Shared fixtures
```

**Example Test:**
```python
import pytest
from fastapi.testclient import TestClient
from system import sapp

client = TestClient(sapp)

def test_login_success():
    """Test successful login"""
    response = client.post(
        "/token",
        data={"username": "admin@fortress.io", "password": "secure123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["role"] == "principal"

def test_login_invalid_credentials():
    """Test login with invalid credentials"""
    response = client.post(
        "/token",
        data={"username": "admin@fortress.io", "password": "wrong"}
    )
    assert response.status_code == 401
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run specific test
pytest tests/test_auth.py::test_login_success
```

---

## 📚 Documentation

### Code Documentation

Use Google-style docstrings:

```python
def create_user(self, user_data: UserEnter, current_user_id: int) -> UserID:
    """
    Create a new user in the system.

    Args:
        user_data: The user data for creation
        current_user_id: ID of the user performing the action

    Returns:
        The created user with assigned ID

    Raises:
        UserAlreadyExistsException: If email already exists
        ForbiddenException: If trying to create principal

    Example:
        >>> user_data = UserEnter(name="John", email="john@example.com", ...)
        >>> new_user = service.create_user(user_data, principal_id)
    """
```

### API Documentation

Update Swagger docs for new endpoints:

```python
@sapp.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Create a new user account. Only principals can create users.",
    responses={
        201: {"description": "User created successfully"},
        400: {"description": "User already exists"},
        403: {"description": "Forbidden - only principals can create users"}
    }
)
async def add_user(...):
    """
    Create a new user with the specified details.
    
    - **name**: User's full name
    - **email**: Unique email address
    - **role**: User role (user/worker, not principal)
    """
```

---

## 🎨 Design Principles

Follow these principles when contributing:

### 1. **Security First**
Always consider security implications. Never compromise on:
- Password security
- Authentication checks
- Authorization validation
- Data exposure

### 2. **Clean Code**
- Write self-documenting code
- Keep functions small and focused
- Avoid code duplication (DRY principle)
- Use meaningful names

### 3. **Performance**
- Consider performance implications
- Use async/await where appropriate
- Optimize database queries
- Profile before optimizing

### 4. **Maintainability**
- Write tests for new features
- Update documentation
- Add comments for complex logic
- Keep dependencies minimal

---

## 🏆 Recognition

Contributors will be recognized in:
- `CONTRIBUTORS.md` file
- GitHub contributors page
- Release notes (for significant contributions)

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

<div align="center">

**Thank you for contributing to Fortress API! 🙏**

Every contribution, no matter how small, makes a difference.

[⬆ Back to Top](#contributing-to-fortress-api-)

</div>
