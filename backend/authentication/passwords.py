import secrets
ALPHABET = "ABCDEFGHJKLMNOPQRSTUVWXYZabcdefghjklmnopqrstuvwxyz23456789"

def generate_temporary_password(length=12):
    while True:
        password = ''.join(secrets.choice(ALPHABET) for _ in range(length))
        if (any(c.islower() for c in password) and
                any(c.isupper() for c in password) and
                any(c.isdigit() for c in password)):
            return password
