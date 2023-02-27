from typing import Optional

import bcrypt


def hash_password(password: str, salt: Optional[str] = None) -> tuple[str, str]:
    if salt is None:
        salt = bcrypt.gensalt().decode()

    return bcrypt.hashpw(password.encode(), salt.encode()).decode(), salt


def check_password(password: str, hashed_password: str):
    return bcrypt.checkpw(
        password=password.encode(), hashed_password=hashed_password.encode()
    )
