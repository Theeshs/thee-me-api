import bcrypt


def set_password_hash(password: str) -> str:
    password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return password.decode("utf-8")


async def match_password(password_to_check: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        password_to_check.encode("utf-8"), hashed_password.encode("utf-8")
    )
