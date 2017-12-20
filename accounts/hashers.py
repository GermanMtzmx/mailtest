from django.contrib.auth.hashers import PBKDF2PasswordHasher as PBKDF2PassHasher


class PBKDF2PasswordHasher(PBKDF2PassHasher):
    """PBKDF2 password hasher"""

    iterations = 100000
