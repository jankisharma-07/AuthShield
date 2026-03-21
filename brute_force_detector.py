import time

attempts = {}
locked_accounts = {}
LOCK_TIME = 30  # seconds

def record_attempt(username):
    attempts[username] = attempts.get(username, 0) + 1

def is_locked(username):
    if username in locked_accounts:
        if time.time() < locked_accounts[username]:
            return True
        else:
            del locked_accounts[username]  # unlock after time
    return False

def lock_account(username):
    locked_accounts[username] = time.time() + LOCK_TIME

def is_suspicious(username):
    return attempts.get(username, 0) >= 3

def reset_attempts(username):
    if username in attempts:
        del attempts[username]