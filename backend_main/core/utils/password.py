from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from core.utils.env import get_env_variable

_ph = PasswordHasher()


def hash_password(plain_password: str) -> str:
    pepper = get_env_variable("ARGON2_PEPPER")
    return _ph.hash(plain_password + pepper)


def verify_password(plain_password: str, hash_password_from_psql: str) -> bool:
    pepper = get_env_variable("ARGON2_PEPPER")
    try:
        return _ph.verify(hash_password_from_psql, plain_password + pepper)
    except VerifyMismatchError:
        return False
