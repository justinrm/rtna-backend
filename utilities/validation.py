import re

def is_valid_email(email: str) -> bool:
    """
    Validate email format.
    """
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(email_regex, email) is not None

def is_strong_password(password: str) -> bool:
    """
    Validate password strength.
    - At least 8 characters.
    - Contains an uppercase letter, a lowercase letter, a digit, and a special character.
    """
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

def sanitize_input(value: str) -> str:
    """
    Sanitize input by removing potentially harmful characters.
    """
    return re.sub(r"[^\w\s\-.,@#]", "", value)

def is_valid_url(url: str) -> bool:
    """
    Validate URL format.
    """
    url_regex = r"^(http|https)://[^\s/$.?#].[^\s]*$"
    return re.match(url_regex, url) is not None

