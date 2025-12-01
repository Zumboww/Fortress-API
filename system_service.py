from typing import List, Optional
from system_schema import Gender, Role, UserID, UserEnter, UserUpdate
from system_exceptions import (
    UserNotFoundException, UserAlreadyExistsException, EmailNotMatchException, 
    ForbiddenException, PrincipalProtectedException, PrincipalAlreadyExistsException
)
import polars as pl
from system_utils import get_password_verify, get_password_hash

class UserService:
    """Service layer for managing user operations"""

    def __init__(self, csv_path: str = "users.csv"):
        self.csv_path = csv_path
        self.users: List[UserID] = []
        self._load_users_from_csv(csv_path)
        self._validate_principal_uniqueness()

    def _load_users_from_csv(self, csv_path: str) -> None:
        """Load users from CSV file"""
        try:
            sd = pl.read_csv(csv_path, infer_schema_length=None, encoding="UTF-8")
            self.users = [
                UserID(
                    user_id=i + 1,
                    name=row[0],
                    age=int(row[1]),
                    gender=Gender(row[2]),
                    email=row[3],
                    password=row[4],  # Load password from CSV
                    role=Role(row[5]) if len(row) > 5 else Role.User  # Load role from CSV, default to User
                )
                for i, row in enumerate(sd.rows())
            ]
            print(f"✓ Loaded {len(self.users)} users from CSV")
        except Exception as e:
            print(f"✗ CSV load failed: {e}")
            self.users = []

    def _validate_principal_uniqueness(self) -> None:
        """Validate that only one principal exists in the system"""
        principals = [user for user in self.users if user.role == Role.Principal]
        if len(principals) > 1:
            raise PrincipalAlreadyExistsException()

    def _get_principal_user(self) -> Optional[UserID]:
        """Get the principal user if exists"""
        return next((user for user in self.users if user.role == Role.Principal), None)

    def _save_users_to_csv(self) -> None:
        """Save users to CSV file"""
        try:
            # Create DataFrame from users
            data = {
                "name": [user.name for user in self.users],
                "age": [user.age for user in self.users],
                "gender": [user.gender for user in self.users],
                "email": [user.email for user in self.users],
                "password": [user.password for user in self.users],
                "role": [user.role for user in self.users]
            }
            df = pl.DataFrame(data)
            df.write_csv(self.csv_path)
            print(f"✓ Saved {len(self.users)} users to CSV")
        except Exception as e:
            print(f"✗ CSV save failed: {e}")
            raise

    def get_all_users(self, length: Optional[int] = None, offset: Optional[int] = None) -> List[UserID]:
        """Get users with optional pagination"""
        start = (offset - 1) if offset is not None else 0

        if length is not None:
            return self.users[start:start + length]
        return self.users[start:]

    def get_user_by_id(self, user_id: int) -> UserID:
        """Find a user by ID"""
        user = next((s for s in self.users if s.user_id == user_id), None)
        if not user:
            raise UserNotFoundException()
        return user

    def create_user(self, user_data: UserEnter) -> UserID:
        """Create a new user"""
        # PRINCIPAL PROTECTION: Prevent creating another principal if one already exists
        if user_data.role == Role.Principal:
            principal = self._get_principal_user()
            if principal:
                raise PrincipalAlreadyExistsException()

        # Check if email already exists
        if any(s.email == user_data.email for s in self.users):
            raise UserAlreadyExistsException()

        # Generate new ID
        new_id = max((s.user_id for s in self.users), default=0) + 1

        # Hash the password before storing
        hashed_password = get_password_hash(user_data.password)

        # Create new user
        new_user = UserID(
            user_id=new_id,
            name=user_data.name,
            age=user_data.age,
            gender=user_data.gender,
            email=user_data.email,
            password=hashed_password,  # Store hashed password
            role=user_data.role  # Include role
        )

        self.users.append(new_user)
        self._save_users_to_csv()  # Persist to CSV
        print(f"✓ Created user: {new_user.name} (ID: {new_id})")
        return new_user

    def update_user(self, user_id: int, user_update: UserUpdate, current_user_role: str, current_user_id: int) -> UserID:
        """Full update of a user (PUT)"""
        target_user = next((s for s in self.users if s.user_id == user_id), None)

        if not target_user:
            raise UserNotFoundException()

        # Check email conflict (if trying to change email to one that exists)
        if user_update.email and user_update.email != target_user.email:
            if any(s.email == user_update.email for s in self.users):
                raise EmailNotMatchException()

        # Update all fields
        for key, value in user_update.model_dump().items():
            if hasattr(target_user, key) and value is not None:
                # PRINCIPAL PROTECTION: Prevent changing principal's role
                if key == "role":
                    if target_user.role == Role.Principal:
                        raise PrincipalProtectedException("Principal user's role cannot be changed")
                    if current_user_role != "principal":
                        raise ForbiddenException("Only principals can change user roles")
                # SECURITY: Only principals can change emails (authentication credential)
                # Users can change their own email, principals can change any email
                if key == "email":
                    if current_user_role != "principal" and current_user_id != user_id:
                        raise ForbiddenException("Only principals can change other users' emails")
                # Hash password if it's being updated
                if key == "password":
                    value = get_password_hash(value)
                setattr(target_user, key, value)

        self._save_users_to_csv()  # Persist to CSV
        print(f"✓ Updated user: {target_user.name} (ID: {user_id})")
        return target_user

    def patch_user(self, user_id: int, user_patch: UserUpdate, current_user_role: str, current_user_id: int) -> UserID:
        """Partial update of a user (PATCH)"""
        target_user = next((s for s in self.users if s.user_id == user_id), None)

        if not target_user:
            raise UserNotFoundException()

        # PRINCIPAL PROTECTION: Prevent changing principal's role
        if target_user.role == Role.Principal and user_patch.role and user_patch.role != Role.Principal:
            raise PrincipalProtectedException("Principal user's role cannot be changed")

        # Check email conflict (if trying to change email to one that exists)
        if user_patch.email and user_patch.email != target_user.email:
            if any(s.email == user_patch.email for s in self.users):
                raise EmailNotMatchException()

        # Update only provided fields (not None)
        for key, value in user_patch.model_dump().items():
            if hasattr(target_user, key) and value is not None:
                # PRINCIPAL PROTECTION: Prevent changing principal's role
                if key == "role":
                    if target_user.role == Role.Principal:
                        raise PrincipalProtectedException("Principal user's role cannot be changed")
                    if current_user_role != "principal":
                        raise ForbiddenException("Only principals can change user roles")
                # SECURITY: Only principals can change emails (authentication credential)
                # Users can change their own email, principals can change any email
                if key == "email":
                    if current_user_role != "principal" and current_user_id != user_id:
                        raise ForbiddenException("Only principals can change other users' emails")
                # Hash password if it's being updated
                if key == "password":
                    value = get_password_hash(value)
                setattr(target_user, key, value)

        self._save_users_to_csv()  # Persist to CSV
        print(f"✓ Patched user: {target_user.name} (ID: {user_id})")
        return target_user

    def delete_user(self, user_id: int) -> None:
        """Delete a user"""
        target_user = next((s for s in self.users if s.user_id == user_id), None)

        if not target_user:
            raise UserNotFoundException()

        # PRINCIPAL PROTECTION: Prevent deleting principal user
        if target_user.role == Role.Principal:
            raise PrincipalProtectedException("Principal user cannot be deleted")

        self.users.remove(target_user)
        self._save_users_to_csv()  # Persist to CSV
        print(f"✓ Deleted user: {target_user.name} (ID: {user_id})")

    def get_users_count(self) -> int:
        """Get total number of users"""
        return len(self.users)
    
    async def authenticate_user(self, username: str, password: str) -> Optional[UserID]:
        """Authenticate user by email and password"""
        user = next((s for s in self.users if s.email == username), None)
        if not user:
            return None
        if not get_password_verify(password, user.password):
            return None
        return user