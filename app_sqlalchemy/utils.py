from passlib.context import CryptContext
from .schemas import CreateUser

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def pwd_hash_middleware(user_request: CreateUser) -> CreateUser:
    """
    Get the user request for user creation, encrypts the password and returns the same request object with the password
    encrypted.
    """
    hashed_password = password_context.hash(user_request.password)
    user_request.password = hashed_password
    return user_request
