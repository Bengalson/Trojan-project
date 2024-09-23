import os


def secret_key():
    return os.urandom(32)
