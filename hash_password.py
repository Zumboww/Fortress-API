#!/usr/bin/env python3
"""
Password Hashing Utility for Fortress API
This script helps you generate Argon2 hashed passwords for users.csv
"""

from passlib.context import CryptContext
import getpass
import sys

# Initialize password context with Argon2
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password using Argon2"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def main():
    print("🔐 Fortress API - Password Hashing Utility")
    print("=" * 50)
    print()
    
    while True:
        print("Options:")
        print("1. Hash a new password")
        print("2. Verify a password against a hash")
        print("3. Exit")
        print()
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == "1":
            # Hash a password
            print()
            password = getpass.getpass("Enter password to hash: ")
            
            if len(password) < 8:
                print("❌ Password must be at least 8 characters long!")
                print()
                continue
            
            confirm_password = getpass.getpass("Confirm password: ")
            
            if password != confirm_password:
                print("❌ Passwords don't match!")
                print()
                continue
            
            hashed = hash_password(password)
            print()
            print("✅ Password hashed successfully!")
            print()
            print("Hashed password:")
            print("-" * 50)
            print(hashed)
            print("-" * 50)
            print()
            print("Copy this hash to your users.csv file")
            print()
            
        elif choice == "2":
            # Verify a password
            print()
            password = getpass.getpass("Enter plain password: ")
            hashed = input("Enter hashed password: ").strip()
            
            if verify_password(password, hashed):
                print("✅ Password is valid!")
            else:
                print("❌ Password is invalid!")
            print()
            
        elif choice == "3":
            print()
            print("👋 Goodbye!")
            sys.exit(0)
            
        else:
            print("❌ Invalid choice! Please enter 1, 2, or 3")
            print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print()
        print("👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
