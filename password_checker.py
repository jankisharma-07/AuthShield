import random
import string

def check_password_details(password):
    errors = []

    if len(password) < 8:
        errors.append("Minimum 8 characters required")
    if not any(c.isupper() for c in password):
        errors.append("At least one uppercase letter required (A-Z)")
    if not any(c.islower() for c in password):
        errors.append("At least one lowercase letter required (a-z)")
    if not any(c.isdigit() for c in password):
        errors.append("At least one number required (0-9)")
    if not any(c in "!@#$%^&*" for c in password):
        errors.append("At least one special character required (!@#$%^&*)")

    return errors

def suggest_password():
    letters = string.ascii_letters
    digits = string.digits
    symbols = "!@#$%^&*"

    password = [
        random.choice(string.ascii_uppercase),
        random.choice(string.ascii_lowercase),
        random.choice(digits),
        random.choice(symbols)
    ]

    password += random.choices(letters + digits + symbols, k=4)

    random.shuffle(password)
    return ''.join(password)
